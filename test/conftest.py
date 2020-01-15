import logging
import re
import os
import pytest
from freshsalessdk import FreshsalesSDK

logger = logging.getLogger(__name__)

@pytest.fixture
def fs():
    assert os.getenv('FS_DOMAIN') is not None, 'FS_DOMAIN is not set'
    assert os.getenv('FS_API_KEY') is not None, 'FS_DOMAIN is not set'
    return FreshsalesSDK(
        domain=os.getenv('FS_DOMAIN'),
        api_key=os.getenv('FS_API_KEY')
    )
