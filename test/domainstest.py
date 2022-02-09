import os,sys

import unittest

from unittest.mock import patch
from unittest.mock import Mock
from unittest.mock import MagicMock

sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()


from domains import processor
from storage.interface import StorageInterface 


from time import time
test_time = int(time())


class MockStorage(StorageInterface):
        
        storage = {
            'example.com' : []
        }

        def get_domain_id(self,domain : str)  -> int  :
            return 1

        def save_clicks(self, domain_id:int, timestamp: int, clicks: int):
            self.storage['example.com'].append((timestamp,clicks))

        def get_clicks(self,period):
            for d in self.storage.keys():
                for c in self.storage[d]:
                    yield (d,c)

class TestDomains(unittest.TestCase):

    def test_processor(self):
        logger.debug("[TEST][Domains] Test processor ")

        domains = processor(MockStorage())
        domains.add(test_time,'example.com',10)

        for p in domains.get(10):
            self.assertEqual(p[0],'example.com')
            self.assertEqual(p[1][0],test_time)
            self.assertEqual(p[1][1],10)


if __name__ == '__main__':
    unittest.main()


