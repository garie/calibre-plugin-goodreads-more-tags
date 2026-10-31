# Agent guide: Goodreads More Tags

A calibre metadata-source plugin that turns Goodreads shelves into tags. This is a fork of
[MaienM/calibre-plugin-goodread-more-tags](https://github.com/MaienM/calibre-plugin-goodread-more-tags), which has
had no commits since v1.2.1.

## How the plugin works, and why it breaks

- `src/goodreads_more_tags/` is the whole plugin. Everything else is tooling.
- `worker.py` fetches `https://www.goodreads.com/book/shelves/<goodreads id>` and reads each `div.shelfStat`: the
  shelf name from `a.actionLinkLite`, the reader count from the text of `div.smallText` (e.g. `9,692 people`). The
  page needs no login. Shelves are mapped to tags and filtered by the thresholds in the settings.
- `goodreads_integration.py` hooks into the separate **Goodreads** metadata plugin by monkeypatching
  `Goodreads.identify`, `Worker.__init__`, and `Worker.run` in `calibre_plugins.goodreads`. It needs
  `Goodreads.id_from_url` and the worker's `url`, `plugin`, `log`, and `result_queue` attributes.
- `config.py` is the settings dialog, which holds the shelf → tag mapping. It subclasses calibre's
  `calibre.gui2.metadata.config.ConfigWidget` and rearranges its internals: `self.overl`, `self.gb`,
  `self.fields_view`, and `self.l` (a `QGridLayout`). Get calibre's layouts through `QWidget.layout()`, not attribute
  names: calibre already made one of them a local variable once.

Breakage comes from outside the plugin, and it has two causes. The issue labels match:

- `compat-calibre`: calibre or Qt changed under the plugin (Qt6 port, `ConfigWidget` internals). The settings dialog
  is the usual casualty.
- `compat-goodreads`: Goodreads changed its pages, or the Goodreads plugin changed the internals the hook relies on.
  To diagnose, fetch a shelves page with `curl` and compare its markup with the XPaths in `worker.py`.

## Qt and calibre gotchas

- Import Qt names from `PyQt5.Qt` (calibre's compatibility shim). `from PyQt5 import Qt` fails on calibre 6+.
- Qt6 removed `QRegExp` and `QRegExpValidator` (use the `QRegularExpression` versions) and the `Qt.ItemFlags(...)`
  wrapper. `QTableWidgetItem.UserType` is now `QTableWidgetItem.ItemType.UserType`.
- Unscoped enums such as `Qt.StrongFocus` work inside the calibre GUI but raise `AttributeError` under plain
  `calibre-debug -c`. A failure there is not proof the GUI fails.
- Likewise, `calibre-customize -l` can fail to load a plugin that loads fine in the GUI. The authority on whether a
  plugin loads is calibre's plugin dialog: it lists only plugins that loaded.
- The code still has Python 2 leftovers such as `from __future__` imports. Watch for others like `e.message`.

## Testing

Run the pytest suite with `scripts/pytest.sh` (arguments go to pytest, e.g. `scripts/pytest.sh tests/test_config.py`).
Bare `pytest` or `uv run pytest` can't import calibre and stops with a usage error. The script:

- runs pytest inside `calibre-debug`, because calibre's modules only import from its own frozen Python. pytest comes
  from `.venv`, which the script creates with `uv` at calibre's Python version (3.14 for calibre 9).
- installs `src/goodreads_more_tags` and the Goodreads plugin into a throwaway `CALIBRE_CONFIG_DIRECTORY`, so your
  real calibre config is never touched. The Goodreads plugin comes from your calibre config unless
  `GOODREADS_PLUGIN_ZIP` is set. `CALIBRE_BIN` overrides where calibre's tools are found.

Things that follow from running inside calibre:

- calibre's Python runs with `-OO`: plain `assert` in non-test modules is a no-op, and docstrings are stripped, which
  is why `tests/test_doctests.py` exists in place of `--doctest-modules`. Put assertions in test modules or conftest,
  which pytest rewrites.
- No `pytest-xdist`: its workers start `sys.executable`, which here is `calibre-debug`.
- No useful `--cov`: tests exercise the copy calibre installed as `calibre_plugins.goodreads_more_tags`, never `src/`.

The suite currently has failures in the identify tests, which hit goodreads.com live or replay outdated recorded pages.
Check the [`tests` issues](https://github.com/garie/calibre-plugin-goodreads-more-tags/issues?q=label%3Atests) before
treating a failure as new. It has been run on macOS only, not Linux.

The suite doesn't cover the settings dialog or real scraping. Check those by hand:

1. Build a zip (see below) and install it in calibre.
2. **Settings dialog:** Preferences → Metadata download → select Goodreads More Tags → Configure selected source.
   This can only be checked in the real calibre window.
3. **Scraping:** in Edit metadata (single book) → Download metadata, open the log and look for `[GoodreadsMoreTags]`
   lines (`Found shelves`, `Tags after mapping`). Cancel so nothing is written.

## Installing

calibre loads plugins from zips in its config directory's `plugins/` folder (`~/Library/Preferences/calibre/plugins/`
on macOS) and reads them only at startup.

**From a release:** download `Goodreads.More.Tags.zip` from the
[releases page](https://github.com/garie/calibre-plugin-goodreads-more-tags/releases), then in calibre go to
Preferences → Plugins → **Load plugin from file**. It replaces an installed copy of the same name (calibre matches on
the plugin's declared name) and keeps its settings, which live in a separate file. Restart calibre.

**From source:** build the zip, then either load it as above or install from the command line:

```sh
scripts/zip-release.sh        # writes Goodreads.More.Tags.zip in the repo root (*.zip is gitignored)
calibre-customize -a Goodreads.More.Tags.zip
```

- On macOS, calibre's command-line tools are in `/Applications/calibre.app/Contents/MacOS/`, not on `PATH`.
- Quit calibre before using `calibre-customize -a`. calibre rewrites its plugin config on exit and can clobber a
  plugin installed while it was running. Load plugin from file is safe while calibre is open.
- To check that a build loads without touching your real setup, point `CALIBRE_CONFIG_DIRECTORY` at a throwaway
  directory.
- `scripts/kill-and-run.sh` runs `pkill -9 -f calibre` before reinstalling.

**The plugin updater can't follow this repo.** calibre's updater reads one hardcoded index
(`https://code.calibre-ebook.com/plugins/plugins.json.bz2`), with no setting for other sources or per-plugin update
URLs. The index serves the zip attached to the first post of the
[MobileRead thread](https://www.mobileread.com/forums/showthread.php?p=3875236), which is still 1.2.1.2. Getting a fork
release into the updater means having that attachment replaced, which only the thread's owner or a MobileRead
moderator can do. Until then, install from this repo's releases. Fork versions sort above the index's 1.2.1.2, so the
updater won't offer to replace them unless the index publishes a higher version.

## Versions, tags, and releases

Fork versions add a fourth component to upstream's last release: `1.2.1.3`, `1.2.1.4`, and so on.

1. **One commit per fix.** If an issue tracks it, end the commit body with `Fixes #N` so pushing to `main` closes it.
2. **A tagging commit**, following upstream's pattern: subject `Tagging vX`. It bumps `version` in
   `src/goodreads_more_tags/__init__.py` and adds a README "Version History" entry. That section is a changelog: list
   what changed in the version, not open bugs.
3. **An annotated tag** `vX` on the tagging commit:

   ```
   Version X

   - <one bullet per change, matching the README entry, with (#N) where an issue exists>
   ```

4. **A GitHub release** for the tag, created with `gh release create vX --verify-tag`:
   - Title: a short summary of the version.
   - Notes: the tag message's bullets.
   - Asset: `Goodreads.More.Tags.zip`, built from the tag, not from a working tree:

     ```sh
     tmp=$(mktemp -d)
     git archive vX src/goodreads_more_tags | tar -x -C "$tmp"
     (cd "$tmp/src/goodreads_more_tags" && zip -r ../../Goodreads.More.Tags.zip . --exclude '*.pyc')
     ```

   - Check the asset: download it back with `gh release download` and compare its contents with the tag.
   - Mark the newest version as latest.

Existing tags:

- `v1.0.0` to `v1.2.1` are upstream's lightweight tags. Never move, re-create, or annotate them.
- `v1.2.1.2` sits on the commit that imported the plugin index's zip verbatim, not on a tagging commit, and its release
  asset is that zip's original bytes. Leave both as they are.

## Issues

Labels:

- `bug`: the plugin misbehaves for users. Add `compat-calibre` or `compat-goodreads` for the cause.
- `enhancement`: something that doesn't exist yet.
- `tests`: the test suite and dev tooling. Usually paired with `enhancement`, since the plugin itself isn't broken.

An issue describes what happens and why. The fix belongs in the commit that closes it.

## README

`scripts/readme-to-vbcode.py` converts `README.md` into the MobileRead post format, so the README is written for
plugin users, not contributors.
