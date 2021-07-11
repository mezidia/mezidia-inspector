import gidgethub.routing

from .utils import get_token, leave_comment, fields, help_issue_update, get_url_for_deleted_branch

router = gidgethub.routing.Router()


@router.register('pull_request', action='opened')
async def pr_opened(event, gh, *args, **kwargs):
    """Opened pull request"""
    comment_url = event.data['pull_request']['comments_url']
    sender = event.data['sender']['login']
    file_url = event.data['repository']['html_url'] + '/CONTRIBUTING.md'
    author_association = event.data['pull_request']['author_association']
    token = await get_token(event, gh)
    comment = f'Nice to meet you, @{sender}. Thank you for creating a pull request.\n'
    if author_association == 'NONE':
        comment += f"It's your first contribution, so read [CONTRIBUTING.md]({file_url}), if you didn't do this.\n"
    comment += 'There are some tasks for you:\n'
    if token is not None:
        for field in fields:
            comment += f"- {'[x]' if event.data['pull_request'][field['field_name']] else '[ ]'} {field['field_text']}\n"
        comment += f"- {'[x]' if event.data['pull_request']['draft'] == 'true' else '[ ]'} " \
                f"{'Make a pull request draft at first'}\n"
        comment += '\nTo close issue send comment "close", to reopen - "reopen", to merge - "merge"'
        
        return await leave_comment(gh, comment_url, comment, token['token'])
    else:
        return await gh.post(comment_url)


@router.register('pull_request', action='closed')
@router.register('pull_request', action='merged')
async def pr_closed_merged(event, gh, *args, **kwargs):
    """Closed or merged pull request"""
    token = await get_token(event, gh)
    created_by = event.data['pull_request']['user']['login']
    comment_url = event.data['pull_request']['comments_url']
    info = event.data['pull_request']['head']
    comment = ''
    if event.data['pull_request']['merged'] and event.data['pull_request']['state'] == 'closed':
        merged_by = event.data['pull_request']['merged_by']['login']
        if created_by == merged_by or merged_by == 'mezidia-inspector':
            comment = f'Thanks @{created_by} for the PR 🌮🎉.'
        else:
            comment = f'Thanks @{created_by} for the PR, and @{merged_by} for merging it 🌮🎉.'
        branch_url = await get_url_for_deleted_branch(info)
        if token is not None:
            await gh.delete(branch_url, oauth_token=token['token'],)
        else:  # For tests
            return await gh.delete(branch_url)
    else:
        comment = f'Okay, @{created_by}, see you next time\n'
        comment += '> To reopen pull request type the comment "reopen"'
    return await leave_comment(gh, comment_url, comment, token['token'])


@router.register('pull_request', action='labeled')
@router.register('pull_request', action='converted_to_draft')
@router.register('pull_request', action='assigned')
@router.register('pull_request', action='milestoned')
async def pr_task_update(event, gh, *args, **kwargs):
    if await help_issue_update(event, 'pull_request'):
        token = await get_token(event, gh)
        comment_url = event.data['pull_request']['comments_url']
        comment = 'Nice, one of tasks is done'
        return await leave_comment(gh, comment_url, comment, token['token'])
