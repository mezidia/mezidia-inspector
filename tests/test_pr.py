from gidgethub import sansio

from inspector import prs
from .gh import FakeGH

test_number = 5772
admin_nickname = 'mezgoodle'
bot_name = 'mezgoodle-bot'
test_ref = 'backport-17ab8f0-3.7'
test_repo_name = 'some_name'
issue_url = 'https://api.github.com/issue/123'


async def test_pr_opened():
    """Test opened pull request"""
    data = {
        'action': 'opened',
        'pull_request': {
            'number': test_number,
            'author_association': 'owner',
            'comments_url': issue_url,
            'state': 'closed',
        },
        'sender': {'login': admin_nickname},
        'repository': {'html_url': 'https://'}
    }
    event = sansio.Event(data, event='pull_request', delivery_id='1')

    gh = FakeGH()
    await prs.router.dispatch(event, gh)
    assert gh.post_url == f'{issue_url}'


async def test_branch_deleted_when_pr_merged():
    """Test merged pull request"""
    data = {
        'action': 'closed',
        'pull_request': {
            'number': test_number,
            'user': {'login': bot_name},
            'merged': True,
            'merged_by': {'login': admin_nickname},
            'head': {
                'ref': test_ref, 'user': {'login': admin_nickname},
                'repo': {'name': test_repo_name}
            },
            'comments_url': issue_url,
            'state': 'closed',
        },
    }
    event = sansio.Event(data, event='pull_request', delivery_id='1')

    gh = FakeGH()
    await prs.router.dispatch(event, gh)
    assert gh.post_data is None
    assert (
            gh.delete_url
            == f'/repos/{admin_nickname}/{test_repo_name}/git/refs/heads/{test_ref}'
    )
