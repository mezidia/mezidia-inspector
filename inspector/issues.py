"""Issues trigger"""

import gidgethub.routing

from .utils import get_token, leave_comment, update_issue, states

router = gidgethub.routing.Router()

fields = [
    {
        'field_name': 'labels',
        'field_text': 'Need at least one label',
    },
    {
        'field_name': 'assignees',
        'field_text': 'Need at least one assignee',
    },
    {
        'field_name': 'milestone',
        'field_text': 'Need a milestone',
    }
]


@router.register('issue_comment', action='created')
async def issue_comment_created(event, gh, *args, **kwargs):
    """Created issue comment"""
    comment_text = event.data['comment']['body'].lower().strip()
    if comment_text in states:
        username = event.data['sender']['login']
        token = await get_token(event, gh)
        issue_url = event.data['issue']['url']
        issue_comment_url = event.data['issue']['comments_url']
        await update_issue(gh, issue_url, comment_text, token['token'])
        await leave_comment(gh, issue_comment_url, f'@{username}, I updated the issue', token['token'])


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
    await leave_comment(gh, url, comment, token['token'])


@router.register('issues', action='closed')
async def issue_closed(event, gh, *args, **kwargs):
    token = await get_token(event, gh)
    comment_url = event.data['issue']['comments_url']
    author = event.data['issue']['user']['login']
    sender = event.data['sender']['login']

    comment = f'Thanks for issue, @{author}! @{sender}, thank \
    you for closing this issue, I have less work. \
    I will look forward to our next meeting😜\n'
    comment += f'> If you want to reopen the issue - type "reopen"'

    await leave_comment(gh, comment_url, comment, token['token'])
