######################################################################
# Additional tests to push coverage over 95%
######################################################################

import unittest

from wsgi import app
from service.common import status


BASE_URL = "/api/promotions"


class TestCoverageBoost(unittest.TestCase):
    """Coverage boost tests"""

    def setUp(self):
        self.client = app.test_client()

    def test_invalid_content_type_returns_415(self):
        """It should return 415 for wrong content type"""
        response = self.client.post(
            BASE_URL,
            data='{"name":"bad"}',
            content_type="text/plain",
        )
        self.assertEqual(
            response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        )