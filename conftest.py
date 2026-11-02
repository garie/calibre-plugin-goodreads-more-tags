from __future__ import unicode_literals

import sys

import pytest

from tests.fixture_browser import browser, no_headless_browsers
from tests.fixture_configs import *
from tests.fixture_fix_underscore import fix_underscore
from tests.fixture_generic import *
from tests.fixture_identify import identify

# calibre's modules are only importable from its own interpreter; see scripts/pytest.sh.
if 'calibre' not in sys.modules:
    raise pytest.UsageError('Run the tests with scripts/pytest.sh, which runs them inside calibre-debug.')

# Import all plugins. Without this, calibre_plugins imports don't work.
from calibre.customize.ui import all_metadata_plugins  # noqa


collect_ignore = [
    'scripts/',
]

