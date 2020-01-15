import logging
import re
import pytest

logger = logging.getLogger(__name__)

@pytest.fixture
def accounts_view_id(fs):
    views = fs.accounts.get_views()
    for v in views:
        if re.match('all', v['name'].lower()):
            return v['id']
    assert False, 'Could not find a accounts view'

def assert_account_well_formed(account):
    logger.debug('checking account %s', account)
    assert set(['id', 'name', 'owner']) - set(account.keys()) == set([]), 'some keys are missing'

def test_accounts_get_views(fs):
    views = fs.accounts.get_views()
    assert views

def test_accounts_get_all_generator(fs, accounts_view_id):
    for account in fs.accounts.get_all_generator(view_id=accounts_view_id, limit=10):
        assert_account_well_formed(account)

def test_accounts_get(fs, accounts_view_id):
    account = next(fs.accounts.get_all_generator(view_id=accounts_view_id, limit=1))
    assert_account_well_formed(account)
