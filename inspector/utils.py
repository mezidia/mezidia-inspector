from gidgethub import apps

from .config import GH_APP_ID, GH_PRIVATE_KEY

states = {
    'close': 'closed',
    'reopen': 'open',
    'merge': {
        'commit_title': 'Merge pull request',
        'commit_message': 'Merged by Mezidia Inspector'
    },
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


async def get_url_for_deleted_branch(info):
    owner = info['user']['login']
    ref = info['ref']
    repo = info['repo']['name']
    url = f'/repos/{owner}/{repo}/git/refs/heads/{ref}'
    return url


async def update_issue(gh, issue_url, comment_text, token):
    if comment_text != 'merge':
        data = {'state': states[comment_text]}
        await gh.post(
            f'{issue_url}',
            data=data,
            oauth_token=token
        )
    else:
        data = {
            'commit_title': states[comment_text]['commit_title'],
            'commit_message': states[comment_text]['commit_message'],
        }
        await gh.put(
            f'{issue_url}',
            data=data,
            oauth_token=token
        )


async def help_issue_update(event, object_type: str):
    actions = {
        'labeled': 'labels',
        'assigned': 'assignees',
    }
    if actions[event.data['action']] == 'converted_to_draft' or actions[event.data['action']] == 'milestoned':
        return True
    if len(event.data[object_type][actions[event.data['action']]]) > 1:
        return False
    return True
