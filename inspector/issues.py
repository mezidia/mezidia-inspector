import gidgethub.routing

from .utils import get_token, leave_comment, update_issue, states, fields, help_issue_update

router = gidgethub.routing.Router()


@router.register('issue_comment', action='created')
async def issue_comment_created(event, gh, *args, **kwargs):
    """Created issue comment"""
    comment_text = event.data['comment']['body'].lower().strip()
    if comment_text in states:
        issue_author = event.data['issue']['user']['login']
        username = event.data['sender']['login']
        if issue_author == username:
            token = await get_token(event, gh)
            issue_comment_url = event.data['issue']['comments_url']
            comment = f'@{username}, I updated the issue'
            if token:
                if comment_text == 'merge':
                    issue_url = event.data['repository']['url']
                    pull_number = event.data['issue']['html_url'].split('/')[-1]
                    issue_url += f'/pulls/{pull_number}/merge'
                    await update_issue(gh, issue_url, comment_text, token['token'])
                else:
                    issue_url = event.data['issue']['url']
                    await update_issue(gh, issue_url, comment_text, token['token'])
                return await leave_comment(gh, issue_comment_url, comment, token['token'])
            else:
                await gh.post(issue_comment_url)


@router.register('issues', action='opened')
async def issue_created(event, gh, *args, **kwargs):
    """Opened issue"""
    token = await get_token(event, gh)
    url = event.data['issue']['comments_url']
    sender = event.data['sender']['login']
    comment = f'Nice to meet you, @{sender}. Thank you for creating an issue. There are some tasks for you:\n'
    for field in fields:
        comment += f"- {'[x]' if event.data['issue'][field['field_name']] else '[ ]'} {field['field_text']}\n"
    comment += '\nTo close issue send comment "close", to reopen - "reopen"'
    return await leave_comment(gh, url, comment, token['token'])


@router.register('issues', action='closed')
async def issue_closed(event, gh, *args, **kwargs):
    """Closed issue"""
    token = await get_token(event, gh)
    comment_url = event.data['issue']['comments_url']
    author = event.data['issue']['user']['login']
    sender = event.data['sender']['login']
    comment = f'Thanks for issue, @{author}! @{sender}, thank \
    you for closing this issue, I have less work. \
    I will look forward to our next meeting😜\n'
    comment += '> If you want to reopen the issue - type "reopen"'
    return await leave_comment(gh, comment_url, comment, token['token'])


@router.register('issues', action='labeled')
@router.register('issues', action='assigned')
@router.register('issues', action='milestoned')
async def issue_task_update(event, gh, *args, **kwargs):
    """Updated issue"""
    if await help_issue_update(event, 'issue'):
        token = await get_token(event, gh)
        comment_url = event.data['issue']['comments_url']
        comment = 'Nice, one of tasks is done'
        return await leave_comment(gh, comment_url, comment, token['token'])
