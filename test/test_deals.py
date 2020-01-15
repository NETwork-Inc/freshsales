import logging
import re
import pytest

logger = logging.getLogger(__name__)

@pytest.fixture
def deals_view_id(fs):
    views = fs.deals.get_views()
    for v in views:
        if re.match('recent', v['name'].lower()):
            return v['id']
    assert False, 'Could not find a deals view with name Recent'

def test_deals_get_views(fs):
    pass

def test_deals_get_all_generator(fs):
    pass

def test_deals_get(fs):
    pass