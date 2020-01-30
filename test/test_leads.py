import logging
import re
import pytest
from .common import dict_read, dict_compare_keys

logger = logging.getLogger(__name__)

@pytest.fixture
def leads_view_id(fs):
    views = fs.leads.get_views()
    for v in views:
        if re.match('all', v['name'].lower()):
            return v['id']
    assert False, 'Could not find a leads view'
    return None

def assert_lead_well_formed(lead):
    ref_lead = dict_read('lead.json')
    logger.debug('lead = %s', lead)
    logger.debug('ref_lead = %s', ref_lead)
    diff = dict_compare_keys(lead, ref_lead)
    logger.debug('dict_compare = %s', diff)
    assert diff == [], 'unexpected lead structure'

def test_leads_get_views(fs):
    views = fs.leads.get_views()
    assert views

def test_leads_get_all_generator(fs, leads_view_id):
    for lead in fs.leads.get_all_generator(view_id=leads_view_id, limit=10):
        assert_lead_well_formed(lead)

def test_lead_get(fs, leads_view_id):
    lead = next(fs.leads.get_all_generator(view_id=leads_view_id, limit=1))
    assert_lead_well_formed(lead)