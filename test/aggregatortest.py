import os,sys

import unittest

from unittest.mock import patch
from unittest.mock import Mock
from unittest.mock import MagicMock

sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()


from aggregation.aggregator import DomainAggregator


testdata = [
    ('example1.com' , (12346,10)),
    ('example2.com' , (12346,5)),
    ('example3.com' , (12346,8)),
    ('example4.com' , (12346,2)),
    ('example1.com' , (12360,22)),
    ('example2.com' , (12360,15)),
    ('example3.com' , (12360,64)),
    ('example4.com' , (12360,4)),
    ('example5.com' , (11000,80)), #Out of date, should not be in counters
]

class TestAggregator(unittest.TestCase):

    aggregator = None

    @patch('time.time', MagicMock(return_value=12345))
    def setUp(self):
        logger.debug("[TEST][AGGREGATOR]Aggregator create")
        self.aggregator = DomainAggregator(3,300)
        self.assertEqual(self.aggregator.next_rebuild,12600)


    @patch('time.time', MagicMock(return_value=12601))
    def test_aggregator_rebuild(self): 
        logger.debug("[TEST][AGGREGATOR] Test aggregator want_rebuild")
        self.assertTrue(self.aggregator.want_rebuild())
        self.aggregator.rebuild(testdata)
        #{'domains': {'example4.com': 6, 'example3.com': 72, 'example2.com': 20, 'example1.com': 32}}
        data = dict(self.aggregator)
        counters  = data['domains']
        self.assertEqual(counters['example1.com'],32)
        self.assertEqual(counters['example2.com'],20)
        self.assertEqual(counters['example3.com'],72)


if __name__ == '__main__':
    unittest.main()


