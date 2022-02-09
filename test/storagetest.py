import os,sys

import unittest

from unittest.mock import patch
from unittest.mock import Mock
from unittest.mock import MagicMock


unittest.TestLoader.sortTestMethodsUsing = None

sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()


from storage import storage
from storage.memory import get_domain_by_id
from time import time

test_time = int(time())


class TestStorage(unittest.TestCase):

    def test_domainid(self):
        logger.debug("[TEST][STORAGE] Test domain_id ")
        domain_id = storage.get_domain_id('example.com')
        self.assertEqual(domain_id,1)
        logger.debug("[TEST][STORAGE] Second request for domain id ")
        domain_id = storage.get_domain_id('example.com')
        self.assertEqual(domain_id,1)

        logger.debug("[TEST][STORAGE] get_domain_by_id ")
        domain = get_domain_by_id(1)
        self.assertEqual(domain,'example.com')
        domain = get_domain_by_id(100)
        self.assertEqual(domain,None)

    def test_save_clicks(self):
        logger.debug("[TEST][STORAGE] Test save clicks ")
        domain_id = storage.get_domain_id('example.com')
        self.assertEqual(domain_id,1)
        storage.save_clicks(domain_id,test_time, 15 )
        storage.save_clicks(domain_id,test_time, 15 )

        logger.debug("[TEST][STORAGE] Test load clicks ")
        count = 0
        for data in storage.get_clicks(10):
            count  = count + 1
            self.assertEqual(data[0],'example.com',"Wrong data domen")
            self.assertEqual(data[1][0],test_time,"Wrong data time")
            self.assertEqual(data[1][1],15,"Wrong clicks count")
        self.assertEqual(count,2,"Wrong records count")

if __name__ == '__main__':
    unittest.main()

