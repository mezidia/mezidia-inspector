from gidgethub import sansio

from inspector import issues
from .gh import FakeGH


async def test_issue_opened():
    """Test issue comment creation"""
    issue_url = 'https://api.github.com/issue/123'
    admin_nickname = 'mezgoodle'
    data = {
        'action': 'created',
        'comment': {
            'url': issue_url,
        },
        'sender': {'login': admin_nickname}
    }
    event = sansio.Event(data, event='issue_comment', delivery_id='1')

    gh = FakeGH()
    await issues.router.dispatch(event, gh)
    assert (
            gh.post_url == f'{issue_url}/comments'
    )
