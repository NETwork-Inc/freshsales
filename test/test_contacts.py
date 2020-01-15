import logging
import re
import pytest
from .common import dict_read, dict_compare_keys

logger = logging.getLogger(__name__)

@pytest.fixture
def contacts_view_id(fs):
    views = fs.contacts.get_views()
    for v in views:
        if re.match('all', v['name'].lower()):
            return v['id']
    assert False, 'Could not find a contacts view'

def assert_contact_well_formed(contact):
    ref_contact = dict_read('contact.json')
    logger.debug('contact = %s', contact)
    logger.debug('ref_contact = %s', ref_contact)
    diff = dict_compare_keys(contact, ref_contact)
    logger.debug('dict_compare = %s', diff)
    assert diff == [], 'unexpected contact structure'

def test_contacts_get_views(fs):
    views = fs.contacts.get_views()
    assert views

def test_contacts_get_all_generator(fs, contacts_view_id):
    for contact in fs.contacts.get_all_generator(view_id=contacts_view_id, limit=10):
        assert_contact_well_formed(contact)

def test_contacts_get(fs, contacts_view_id):
    contact1 = next(fs.contacts.get_all_generator(view_id=contacts_view_id, limit=1))
    assert_contact_well_formed(contact1)
    contact2 = fs.contacts.get(id=contact1['id'])
    assert_contact_well_formed(contact2)
