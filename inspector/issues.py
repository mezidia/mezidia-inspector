"""Issues trigger"""

import gidgethub.routing

from .utils import get_token, leave_comment, update_issue

router = gidgethub.routing.Router()

states = {
    'close': 'closed',
    'reopen': 'reopen',
}


@router.register('issue_comment', action='created')
async def issue_comment_created(event, gh, *args, **kwargs):
    """Created issue comment"""
    print('hello')
    username = event.data['sender']['login']
    token = await get_token(event, gh)
    issue_url = event.data['issue']['url']
    comment_text = event.data['comment']['body']
    await update_issue(gh, issue_url, states[comment_text.lower().strip()], token['token'])
    await leave_comment(gh, issue_url, f'@{username}, I updated the issue', token['token'])


@router.register('issues', action='opened')
async def issue_created(event, gh, *args, **kwargs):
    """Opened issue"""
    pass
    # token = await get_token(event, gh)
    # url = event.data['issue']['comments_url']
    # sender = event.data['sender']['login']
    #
    # if sender == ADMIN_NICKNAME:
    #     msg = 'Nice to meet you here, sensei!'
    # else:
    #     msg = f'Nice to meet you, @{sender}\nI wish you have a nice \
    #     day😊\n@mezgoodle will answer as soon as he can.'
    #
    # await leave_comment(gh, url, msg, token['token'])


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
