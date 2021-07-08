import gidgethub.routing

from .utils import get_token

router = gidgethub.routing.Router()


@router.register('installation', action='created')
async def repo_installation_added(event, gh, *args, **kwargs):
    """Installed bot to repository"""
    token = await get_token(event, gh)
    sender_name = event.data['sender']['login']
    for repo in event.data['repositories']:
        repo_full_name = repo['full_name']
        if token is not None:
            response = await gh.post(
                f'/repos/{repo_full_name}/issues',
                data={
                    'title': 'Thanks for installing me!',
                    'body': f'Greetings from **Mezidia Inspector!**, you are the best! @{sender_name}\n '
                            f'- My code and instructions you can see '
                            f'[here](https://github.com/mezidia/mezidia-inspector).\n'
                            f'- My author is @mezgoodle.\n'
                            f'- This issue was closed immediately.',
                    'labels': ['thank you'],
                    'assignee': sender_name
                },
                oauth_token=token['token'],
            )
            issue_url = response['url']
            await gh.patch(
                issue_url,
                data={'state': 'closed'},
                oauth_token=token['token'],
            )
        else:
            await gh.post(f'/repos/{repo_full_name}/issues')
