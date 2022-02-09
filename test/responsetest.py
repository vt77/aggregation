import os,sys

import unittest

from unittest.mock import patch
from unittest.mock import Mock
from unittest.mock import MagicMock

sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()


from response import Response, Message


class TestResponse(unittest.TestCase):

    def test_message(self):
        logger.debug("[TEST][RESPONSE] Test message ")
        resp =  Response(Message("ERROR"),Response.ERROR)
        data = resp.toJSON()
        self.assertEqual(data['message'],'ERROR')
        self.assertEqual(data['status'],'error')

if __name__ == '__main__':
    unittest.main()


