"""Issues trigger"""

import gidgethub.routing

from .utils import get_token, leave_comment, update_issue

router = gidgethub.routing.Router()

states = {
    'close': 'closed',
    'reopen': 'open',
}

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
    username = event.data['sender']['login']
    token = await get_token(event, gh)
    issue_url = event.data['issue']['url']
    comment_text = event.data['comment']['body']
    await leave_comment(gh, issue_url, f'@{username}, I updated the issue', token['token'])
    await update_issue(gh, issue_url, states[comment_text.lower().strip()], token['token'])


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
    """Opened issue"""
    pass
    # token = await get_token(event, gh)
    # url = event.data['issue']['comments_url']
    # author = event.data['issue']['user']['login']
    # sender = event.data['sender']['login']
    #
    # msg = f'Thanks for issue, @{author}! @{sender}, thank \
    # you for closing this issue, I have less work. \
    # I will look forward to our next meeting😜'
    #
    # await leave_comment(gh, url, msg, token['token'])
