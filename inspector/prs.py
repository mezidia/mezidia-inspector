import gidgethub.routing

from .utils import get_token, leave_comment, fields

router = gidgethub.routing.Router()


@router.register('pull_request', action='opened')
async def pr_opened(event, gh, *args, **kwargs):
    """Opened pull request"""
    issue_comment_url = f"{event.data['pull_request']['issue_url']}/comments"
    sender = event.data['sender']['login']
    file_url = event.data['repository']['html_url'] + '/CONTRIBUTING.md'
    author_association = event.data['pull_request']['author_association']
    token = await get_token(event, gh)
    comment = f'Nice to meet you, @{sender}. Thank you for creating a pull request.\n'
    if author_association == 'NONE':
        comment += f"It's your first contribution, so read [CONTRIBUTING.md]({file_url}), if you didn't do this.\n"
    comment += 'There are some tasks for you:\n'
    for field in fields:
        comment += f"- {'[x]' if event.data['pull_request'][field['field_name']] else '[ ]'} {field['field_text']}\n"
    comment += f"- {'[x]' if event.data['pull_request']['draft'] == 'true' else '[ ]'} " \
               f"{'Make a pull request draft at first'}\n"
    if token is not None:
        await leave_comment(gh, issue_comment_url, comment, token['token'])
    else:
        await gh.post(f'{issue_comment_url}/comments')


@router.register('pull_request', action='closed')
@router.register('pull_request', action='merged')
async def events_pr(event, gh, *args, **kwargs):
    """Closed or merged pull request"""
    pass
    # token = await get_token(event, gh)
    # created_by = event.data['pull_request']['user']['login']
    # issue_comment_url = event.data['pull_request']['issue_url'] + '/comments'
    # info = event.data['pull_request']['head']
    #
    # if event.data['pull_request']['merged'] and event.data['pull_request']['state'] == 'closed':
    #     merged_by = event.data['pull_request']['merged_by']['login']
    #     if created_by == merged_by or merged_by == BOT_NAME:
    #         thanks_to = f'Thanks @{created_by} for the PR 🌮🎉.'
    #     else:
    #         thanks_to = f'Thanks @{created_by} for the PR, and @{merged_by} for merging it 🌮🎉.'
    #     message = f'{thanks_to}\n🐍🍒⛏🤖 I am not robot! I am not robot!'
    #
    #     owner = info['user']['login']
    #     ref = info['ref']
    #     repo = info['repo']['name']
    #     url = f'/repos/{owner}/{repo}/git/refs/heads/{ref}'
    #     if token is not None:
    #         await leave_comment(gh, issue_comment_url, message, token['token'])
    #         await gh.delete(url, oauth_token=token['token'],)
    #     else:  # For tests
    #         await gh.delete(url)
    # else:
    #     message = f'Okey, @{created_by}, see you next time'
    #     owner = info['user']['login']
    #     ref = info['ref']
    #     repo = info['repo']['name']
    #     url = f'/repos/{owner}/{repo}/git/refs/heads/{ref}'
    #     if token is not None:
    #         await leave_comment(gh, issue_comment_url, message, token['token'])
    #         await gh.delete(url, oauth_token=token['token'],)
    #     else:  # For tests
    #         await gh.delete(url)


@router.register('pull_request', action='labeled')
async def labeled_pr(event, gh, *args, **kwargs):
    """Labeled pull request"""
    pass
    # token = await get_token(event, gh)
    # user = event.data['pull_request']['user']['login']
    # sender = event.data['sender']['login']
    # issue_comment_url = event.data['pull_request']['issue_url'] + '/comments'
    # message = f'Wow! New label! @{sender}, thank you a lot! @{user}, did you see it?!'
    # await leave_comment(gh, issue_comment_url, message, token['token'])
