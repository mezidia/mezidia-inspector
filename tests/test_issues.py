from gidgethub import sansio

from inspector import issues
from .gh import FakeGH


async def test_issue_opened():
    """Test issue comment creation"""
    issue_url = 'https://api.github.com/issue/123'
    admin_nickname = 'mezgoodle'
    data = {
        'action': 'created',
        'issue': {'comments_url': issue_url, 'user': {'login': admin_nickname}},
        'sender': {'login': admin_nickname},
        'comment': {'body': 'closE '}
    }
    event = sansio.Event(data, event='issue_comment', delivery_id='1')

    gh = FakeGH()
    await issues.router.dispatch(event, gh)
    assert gh.post_url == issue_url
