"""
Macro for src/releases.md that lists recent GitHub releases.

Enabled in [project.plugins.macros] in zensical.toml. It runs on every build including live-reloads,
so set GH_TOKEN to avoid the unauthenticated API rate limit (60 requests per hour)
"""

import json
import os
import re
import urllib.request
from datetime import datetime
from itertools import islice

REPO = "polpo/picoide"
MAX_RELEASES = 10
ASSET_PATTERN = re.compile(r"^picoide-.*\.zip$")


def fetch_releases():
    request = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/releases?per_page=30",
        headers={"Accept": "application/vnd.github+json"},
    )
    token = os.environ.get("GH_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def demote_headings(markdown):
    """The markdown in the release notes has headings we need to demote below the release's own ## heading"""
    return re.sub(r"^(#{1,4}\s)", r"##\1", markdown, flags=re.MULTILINE)


def render_release(release, asset):
    date = datetime.fromisoformat(release["published_at"].replace("Z", "+00:00"))
    name = release.get("name") or release["tag_name"]
    yield f"## {name} <small>{date:%-d %B %Y}</small> {{ #{release['tag_name']} }}"
    yield (
        f"[:material-download: Download {asset['name']}]({asset['browser_download_url']})"
        "{ .md-button .md-button--primary }"
    )
    body = (release.get("body") or "").strip()
    if body:
        yield demote_headings(body)
    yield f"[Release notes on GitHub]({release['html_url']})"


def downloadable(releases):
    for release in releases:
        if release.get("draft") or release.get("prerelease"):
            continue
        asset = next((a for a in release.get("assets", []) if ASSET_PATTERN.match(a["name"])), None)
        if asset is not None:
            yield release, asset


def releases_list():
    try:
        releases = fetch_releases()
    except Exception as error:
        # fail when running in CI
        if os.environ.get("CI"):
            raise
        return f'!!! warning "Couldn\'t load releases"\n    {error}'

    blocks = (
        block
        for release, asset in islice(downloadable(releases), MAX_RELEASES)
        for block in render_release(release, asset)
    )
    return "\n\n".join(blocks) or "There are no firmware releases yet."


def define_env(env):
    env.macro(releases_list)
