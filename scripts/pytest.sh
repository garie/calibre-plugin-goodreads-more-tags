#!/usr/bin/env bash
#
# Run the test suite inside calibre's Python, against a throwaway calibre config.
#
# Arguments are passed to pytest. Environment:
#   CALIBRE_BIN           directory holding calibre-debug and calibre-customize. Defaults to the directory of
#                         calibre-debug on PATH, or the macOS app bundle.
#   GOODREADS_PLUGIN_ZIP  the Goodreads metadata plugin to test against. Defaults to the copy installed in your
#                         calibre config.

set -euo pipefail
cd "$(dirname "$0")/.."

if [ -z "${CALIBRE_BIN:-}" ]; then
	if command -v calibre-debug > /dev/null; then
		CALIBRE_BIN="$(dirname "$(command -v calibre-debug)")"
	else
		CALIBRE_BIN=/Applications/calibre.app/Contents/MacOS
	fi
fi
calibre_debug="$CALIBRE_BIN/calibre-debug"
calibre_customize="$CALIBRE_BIN/calibre-customize"
[ -x "$calibre_debug" ] || { echo "calibre-debug not found in $CALIBRE_BIN; set CALIBRE_BIN" >&2; exit 1; }

# Run calibre's Python with the real config, before switching to the throwaway one. The plugins print a line on
# import, so keep only the last line.
calibre_python() {
	"$calibre_debug" -c "$1" | tail -n 1
}
python_version="$(calibre_python 'import sys; print("%d.%d" % sys.version_info[:2])')"
if [ -z "${GOODREADS_PLUGIN_ZIP:-}" ]; then
	GOODREADS_PLUGIN_ZIP="$(calibre_python 'from calibre.constants import config_dir; print(config_dir)')/plugins/Goodreads.zip"
fi
[ -f "$GOODREADS_PLUGIN_ZIP" ] || {
	echo "Goodreads plugin not found at $GOODREADS_PLUGIN_ZIP; install it in calibre or set GOODREADS_PLUGIN_ZIP" >&2
	exit 1
}

echo "===== Test dependencies (Python $python_version) ====="
# The packages are imported by calibre's interpreter, so the virtualenv's Python version has to match calibre's.
if [ ! -x .venv/bin/python ] || [ "$(.venv/bin/python -c 'import sys; print("%d.%d" % sys.version_info[:2])')" != "$python_version" ]; then
	uv venv --clear --python "$python_version" .venv
fi
uv pip install --quiet --python .venv/bin/python -r requirements_tests.txt
PYTEST_SITE_PACKAGES="$(.venv/bin/python -c 'import sysconfig; print(sysconfig.get_path("purelib"))')"
export PYTEST_SITE_PACKAGES

echo "===== Installing plugins into a throwaway calibre config ====="
CALIBRE_CONFIG_DIRECTORY="$(mktemp -d)"
export CALIBRE_CONFIG_DIRECTORY
trap 'rm -rf "$CALIBRE_CONFIG_DIRECTORY"' EXIT
"$calibre_customize" --build-plugin src/goodreads_more_tags > /dev/null
"$calibre_customize" --add-plugin "$GOODREADS_PLUGIN_ZIP" > /dev/null

echo "===== Pytest ====="
"$calibre_debug" -e scripts/run-pytest.py -- -vv "$@"
