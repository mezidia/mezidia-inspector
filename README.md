<h1 id="project-title" align="center">
  Mezidia Inspector <img alt="logo" width="40" height="40" src="https://raw.githubusercontent.com/mezgoodle/images/master/MezidiaLogoTransparent.png" /><br>
  <img alt="language" src="https://img.shields.io/badge/language-python-brightgreen?style=flat-square" />
  <img alt="GitHub issues" src="https://img.shields.io/github/issues/mezidia/mezidia-inspector?style=flat-square" />
  <img alt="GitHub closed issues" src="https://img.shields.io/github/issues-closed/mezidia/mezidia-inspector?style=flat-square" />
  <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/mezidia/mezidia-inspector?style=flat-square" />
  <img alt="GitHub closed pull requests" src="https://img.shields.io/github/issues-pr-closed/mezidia/mezidia-inspector?style=flat-square" />
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/mezidia/mezidia-inspector?style=flat-square">
</h1>

<p align="center">
 🌟Hello everyone! This is the repository of the bot on Python "Mezidia Inspector".🌟
</p>

## Motivation :exclamation:

For a long time I did bot for GitHub on my own account. Now I have improved it and done it on behalf of the organization.

## Build status :hammer:

Here you can see build status of [continuous integration](https://en.wikipedia.org/wiki/Continuous_integration)/[continuous deployment](https://en.wikipedia.org/wiki/Continuous_deployment):

[![Python testing](https://github.com/mezidia/mezidia-inspector/actions/workflows/python.yml/badge.svg)](https://github.com/mezidia/mezidia-inspector/actions/workflows/python.yml)
[![{Python} CI](https://gitlab.com/mezgoodle/mezidia-inspector/badges/main/pipeline.svg)](https://gitlab.com/mezgoodle/mezidia-inspector/-/pipelines)
![GitHub deployments](https://img.shields.io/github/deployments/mezidia/mezidia-inspector/mezidia-inspector)

## Badges :mega:

Other badges

[![Platform](https://img.shields.io/badge/Platform-GitHub-brightgreen?style=flat-square)](https://github.com)
[![Bot](https://img.shields.io/badge/Bot-GitHub_App-brightgreen?style=flat-square)](https://docs.github.com/en/developers/apps/getting-started-with-apps/about-apps)
 
## Screenshots :camera:

- Issue responding:

![Screenshot 1](https://raw.githubusercontent.com/mezgoodle/images/master/mezidia-inspector1.png)

- Pull request:

![Screenshot 2](https://raw.githubusercontent.com/mezgoodle/images/master/mezidia-inspector2.png)

- Installation responding:

![Screenshot ](https://raw.githubusercontent.com/mezgoodle/images/master/mezidia-inspector3.png)

## Tech/framework used :wrench:

**Built with**

- [gidgethub](https://gidgethub.readthedocs.io/en/latest/)

## Features :muscle:

With this bot you can **control** and **close** issues and pull requests, **merge** pull requests and **delete** merged branches.

## Code Example :pushpin:

- Main file

```python
import asyncio
import os
import sys
import traceback

import aiohttp
from aiohttp import web
import cachetools
from gidgethub import aiohttp as gh_aiohttp
from gidgethub import routing
from gidgethub import sansio

from . import installation
from . import issues
from . import prs

router = routing.Router(installation.router, issues.router, prs.router)
cache = cachetools.LRUCache(maxsize=500)

routes = web.RouteTableDef()


@routes.get('/', name='home')
async def handle_get(request):
    return web.Response(text='Hello world')


@routes.post('/webhook')
async def webhook(request):
    try:
        body = await request.read()
        secret = os.environ.get('GH_SECRET')
        event = sansio.Event.from_http(request.headers, body, secret=secret)
        if event.event == 'ping':
            return web.Response(status=200)
        async with aiohttp.ClientSession() as session:
            gh = gh_aiohttp.GitHubAPI(session, 'demo', cache=cache)
            await asyncio.sleep(1)
            await router.dispatch(event, gh)
        try:
            print(f'GH requests remaining: {gh.rate_limit.remaining}')
        except AttributeError:
            pass
        return web.Response(status=200)
    except Exception:
        traceback.print_exc(file=sys.stderr)
        return web.Response(status=500)


if __name__ == "__main__":  # pragma: no cover
    app = web.Application()

    app.router.add_routes(routes)
    port = os.environ.get('PORT')
    if port is not None:
        port = int(port)
    web.run_app(app, port=port)
```

## Installation :computer:

To install this app, click on [link](https://github.com/apps/mezidia-inspector).

## Fast usage :dash:

### Docker

1. Build container

```sh
docker build -t mezidia-inspector .
```

2. Start container

```sh
docker run -e GITHUB_TOKEN=<github-token> -e GH_APP_ID=<app-id> -e GH_PRIVATE_KEY=<private-key> -e TELEGRAM_TOKEN=<telegram-token> mezidia-inspector
```

### Python

1. Install dependencies

```sh
pip install -r requirements.txt
```

2. Set environment variables

```sh
set GITHUB_TOKEN=<github-token>
set GH_APP_ID=<app-id>
set GH_PRIVATE_KEY=<private-key>
set TELEGRAM_TOKEN=<telegram-token>
```

3. Run script

```sh
python inspector
```

## API Reference :fireworks:

| Action      | Description | Line of code |
| ----------- | ----------- | ----------- |
| `installation.created`      | After installing the app in repository, bot will create the issue there and close by itself       | [installation.py](https://github.com/mezidia/mezidia-inspector/blob/main/inspector/installation.py#L8-L37) |
| `installation.deleted`   | Bot send message with information about user and repository in [Telegram](https://www.telegram.org/) by this [bot](https://github.com/mezgoodle/github-helper)       | [installation.py](https://github.com/mezidia/mezidia-inspector/blob/main/inspector/installation.py#L40-L48) |
| `issue_comment.created`      | App will only respond on _"close"_, _"reopen"_, _"merge"_ | [issues.py](https://github.com/mezidia/mezidia-inspector/blob/main/inspector/issues.py#L10-L30) |
| `issues.created`      | App will show tasks you need to do after creating the issue | [issues.py](https://github.com/mezidia/mezidia-inspector/blob/main/inspector/issues.py#L33-L43) |
| `issues.closed`      | App will thanks to the author. Leave a comment | [issues.py](https://github.com/mezidia/mezidia-inspector/blob/main/inspector/issues.py#L46-L57) |
| `issues.labeled`, `issues.assigned`, `issues.milestoned`      | App will just leave a comment | [issues.py](https://github.com/mezidia/mezidia-inspector/blob/main/inspector/issues.py#L60-L69) |
| `pull_request.opened`      | App will show tasks you need to do after creating the pull request | [prs.py](https://github.com/mezidia/mezidia-inspector/blob/main/inspector/prs.py#L8-L28) |
| `pull_request.closed`, `pull_request.merged`      | App will thanks to the author. Leave a comment. If it was merged, a merged branch will be deleted | [prs.py](https://github.com/mezidia/mezidia-inspector/blob/main/inspector/prs.py#L31-L54) |
| `pull_request.labeled`, `pull_request.assigned`, `pull_request.milestoned`, `pull_request.converted_to_draft`      | App will just leave a comment | [prs.py](https://github.com/mezidia/mezidia-inspector/blob/main/inspector/issues.py#L57-L66) |

## Tests :microscope:

All tests are [here](https://github.com/mezidia/mezidia-inspector/tree/main/tests) and their results are [here](https://github.com/mezidia/mezidia-inspector/actions/workflows/python.yml).

## Contribute :running:

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Also look at the [CONTRIBUTING.md](https://github.com/mezidia/mezidia-inspector/blob/main/CONTRIBUTING.md).

## Credits :cat::handshake:

- [GitHub bots tutorial](https://github-app-tutorial.readthedocs.io/en/latest/)
- [miss-islington](https://github.com/python/miss-islington)

## License :bookmark:

MIT © [mezidia](https://github.com/mezidia)
