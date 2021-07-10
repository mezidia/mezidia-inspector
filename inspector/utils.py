from gidgethub import apps

from .config import GH_APP_ID, GH_PRIVATE_KEY

states = {
    'close': 'closed',
    'reopen': 'open',
    'merge': '',
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


async def get_token(event, gh):
    if 'installation' in event.data:
        installation_id = event.data['installation']['id']
        token = await apps.get_installation_access_token(
            gh,
            installation_id=installation_id,
            app_id=GH_APP_ID,
            private_key=GH_PRIVATE_KEY
        )
        return token
    else:
        # For testing
        return None


async def leave_comment(gh, issue_comment_url, message, token):
    """Leave comment in issue or pull request"""
    data = {'body': message}
    await gh.post(
        f'{issue_comment_url}',
        data=data,
        oauth_token=token
    )


async def update_issue(gh, issue_url, comment_text, token):
    data = {'state': states[comment_text]}
    await gh.post(
        f'{issue_url}',
        data=data,
        oauth_token=token
    )


async def help_issue_update(event, object_type: str):
    actions = {
        'labeled': 'labels',
        'assigned': 'assignees',
    }
    if len(event.data[object_type][actions[event.data['action']]]) > 1:
        return False
    return True

