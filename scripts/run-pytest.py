"""
Run pytest inside calibre's Python. Use scripts/pytest.sh, which sets up the environment this expects.

calibre's modules can only be imported from its own interpreter, so pytest has to come to calibre: this script runs
under `calibre-debug -e`, and imports pytest from the virtualenv named by PYTEST_SITE_PACKAGES. That virtualenv must
use the same Python version as calibre.
"""
import os
import sys

sys.path.insert(0, os.environ['PYTEST_SITE_PACKAGES'])
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest  # noqa: E402

sys.exit(pytest.main(sys.argv[1:]))
