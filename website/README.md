# PicoIDE website

This is the source for [https://picoide.com/](https://picoide.com/).

The site is built with [Zensical](https://zensical.org/) and Python package management is done with [uv](https://docs.astral.sh/uv/).

## Building

To build, install uv and run:

```
$ uv run zensical build
```

To preview locally with live reload:

```
$ uv run zensical serve
```

The releases list is fetched from the GitHub API on every build, including each live-reload rebuild. Without a token GitHub allows 60 requests an hour so if you hit that, the page shows a warning instead of the list. Run with `GH_TOKEN=$(gh auth token)` to authenticate and raise the limit.

On every push to `main`, GitHub Actions (`.github/workflows/pages.yml`) builds the site and publishes it to GitHub Pages. Publishing, editing or deleting a release also triggers a rebuild (`.github/workflows/releases.yml`).

## License

The PicoIDE documentation source is licensed under the GNU GPL v2 (see LICENSE).
