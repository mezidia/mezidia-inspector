from gidgethub import sansio

from inspector import installation
from .gh import FakeGH


async def test_installation():
    """Test installation feedback"""
    bot_name = 'mezidia-inspector'
    admin_nickname = 'mezgoodle'
    data = {
        'action': 'created',
        'repositories': [{'full_name': bot_name}],
        'sender': {'login': admin_nickname}
    }
    event = sansio.Event(data, event='installation', delivery_id='1')

    gh = FakeGH()
    await installation.router.dispatch(event, gh)
    assert (
            gh.post_url == f'/repos/{bot_name}/issues'
    )
