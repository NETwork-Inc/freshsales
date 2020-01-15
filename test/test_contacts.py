import logging
import re
import pytest

logger = logging.getLogger(__name__)

@pytest.fixture
def contacts_view_id(fs):
    views = fs.contacts.get_views()
    for v in views:
        if re.match('all', v['name'].lower()):
            return v['id']
    assert False, 'Could not find a contacts view'

def assert_contact_well_formed(contact):
    logger.debug('checking contact %s', contact)
    assert set(['id', 'first_name', 'last_name', 'owner', 'sales_accounts']) - set(contact.keys()) == set([]), 'some keys are missing'

def test_contacts_get_views(fs):
    views = fs.contacts.get_views()
    assert views

def test_contacts_get_all_generator(fs, contacts_view_id):
    for contact in fs.contacts.get_all_generator(view_id=contacts_view_id, limit=10):
        assert_contact_well_formed(contact)

def test_contacts_get(fs, contacts_view_id):
    contact = next(fs.contacts.get_all_generator(view_id=contacts_view_id, limit=1))
    assert_contact_well_formed(contact)
