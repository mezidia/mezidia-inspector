from gidgethub import apps

from .config import GH_APP_ID, GH_PRIVATE_KEY

states = {
    'close': 'closed',
    'reopen': 'open',
    'merge': '',
}


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

