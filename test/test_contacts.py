import logging
import re
import pytest

logger = logging.getLogger(__name__)

@pytest.fixture
def contacts_view_id(fs):
    views = fs.contacts.get_views()
    for v in views:
        if re.match('recent', v['name'].lower()):
            return v['id']
    assert False, 'Could not find a contacts view with name Recent'

def test_contacts_get_views(fs):
    pass

def test_contacts_get_all_generator(fs):
    pass

def test_contacts_get(fs):
    pass