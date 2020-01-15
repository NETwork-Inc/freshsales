import logging
import re
import pytest

logger = logging.getLogger(__name__)

@pytest.fixture
def accounts_view_id(fs):
    views = fs.accounts.get_views()
    for v in views:
        if re.match('recent', v['name'].lower()):
            return v['id']
    assert False, 'Could not find a accounts view with name Recent'

def test_accounts_get_views(fs):
    pass

def test_accounts_get_all_generator(fs):
    pass

def test_accounts_get(fs):
    pass