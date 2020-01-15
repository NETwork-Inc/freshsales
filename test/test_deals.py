import logging
import re

import pytest

from .common import dict_compare_keys, dict_read

logger = logging.getLogger(__name__)


@pytest.fixture
def deals_view_id(fs):
    views = fs.deals.get_views()
    for v in views:
        if re.match('all', v['name'].lower()):
            return v['id']
    assert False, 'Could not find a deals view'
    return None


def assert_deal_well_formed(deal):
    ref_deal = dict_read('deal.json')
    logger.debug('deal = %s', deal)
    logger.debug('ref_deal = %s', ref_deal)
    diff = dict_compare_keys(deal, ref_deal)
    logger.debug('dict_compare = %s', diff)
    assert diff == [], 'unexpected deal structure'


def test_deals_get_views(fs):
    views = fs.deals.get_views()
    assert views


def test_deals_get_all_generator(fs, deals_view_id):
    for deal in fs.deals.get_all_generator(view_id=deals_view_id, limit=10):
        assert_deal_well_formed(deal)


def test_deals_get(fs, deals_view_id):
    deal = next(fs.deals.get_all_generator(view_id=deals_view_id, limit=1))
    assert_deal_well_formed(deal)
