import requests

from gidgethub import apps

from .config import GH_APP_ID, GH_PRIVATE_KEY, TELEGRAM_TOKEN

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


async def get_token(event, gh) -> dict:
    """
    Get token for GitHub access
    :param event: webhook event
    :param gh: object with actions
    :return: token
    """
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


async def leave_comment(gh, issue_comment_url: str, message: str, token: str):
    """
    Leave comment in issue or pull request
    :param gh: object with actions
    :param issue_comment_url: api string
    :param message: comment
    :param token: GitHub token
    :return: response
    """
    data = {'body': message}
    return await gh.post(
        f'{issue_comment_url}',
        data=data,
        oauth_token=token
    )


async def get_url_for_deleted_branch(info: dict) -> str:
    """
    Get url for the ref to delete
    :param info: dictionary with meta-information
    :return: api url
    """
    owner = info['user']['login']
    ref = info['ref']
    repo = info['repo']['name']
    url = f'/repos/{owner}/{repo}/git/refs/heads/{ref}'
    return url


async def update_issue(gh, issue_url: str, comment_text: str, token: str):
    """
    Update issue or pr according to hte comment
    :param gh: object with actions
    :param issue_url: api url
    :param comment_text: text
    :param token: GitHub token
    :return: response
    """
    if comment_text != 'merge':
        data = {'state': states[comment_text]}
        return await gh.post(
            f'{issue_url}',
            data=data,
            oauth_token=token
        )
    else:
        data = {
            'commit_title': states[comment_text]['commit_title'],
            'commit_message': states[comment_text]['commit_message'],
        }
        return await gh.put(
            f'{issue_url}',
            data=data,
            oauth_token=token
        )


async def help_issue_update(event, object_type: str) -> bool:
    """
    Some helpful function
    :param event: webhook event
    :param object_type: issue or pr definition
    :return: boolean
    """
    actions = {
        'labeled': 'labels',
        'assigned': 'assignees',
    }
    if event.data['action'] == 'converted_to_draft' or event.data['action'] == 'milestoned':
        return True
    if len(event.data[object_type][actions[event.data['action']]]) > 1:
        return False
    return True


async def send_message_telegram(message: str) -> None:
    """
    Send message to the user by Telegram bot
    :param message: text of message
    :return: nothing to return
    """
    resp = requests.get(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id=353057906'
                        f'&text={message}&parse_mode=Markdown')
    print(resp.status_code)
