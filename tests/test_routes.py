######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
TestPromotion API Service Test Suite
"""

# pylint: disable=duplicate-code
import os
import logging
from unittest import TestCase
from wsgi import app
from service.common import status
from service.models import db, Promotion
from service.utils import PromotionType, _parse_date
from .factories import PromotionFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/promotions"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestYourResourceService(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Promotion).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # ----------------------------------------------------------
    # TEST CREATE
    # ----------------------------------------------------------
    def test_create_promotion(self):
        """It should Create a new Promotion"""
        test_promotion = PromotionFactory()
        logging.debug("Test Promotion: %s", test_promotion.serialize())
        response = self.client.post(BASE_URL, json=test_promotion.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_promotion = response.get_json()
        # self.assertIsInstance(test_promotion.id, str)
        self.assertEqual(new_promotion["id"], test_promotion.id)
        self.assertEqual(new_promotion["name"], test_promotion.name)
        self.assertEqual(
            PromotionType(new_promotion["promotion_type"]),
            test_promotion.promotion_type,
        )
        self.assertEqual(
            _parse_date(new_promotion["start_date"]), test_promotion.start_date
        )
        self.assertEqual(
            _parse_date(new_promotion["end_date"]), test_promotion.end_date
        )
        self.assertEqual(new_promotion["value"], test_promotion.value)
        self.assertEqual(new_promotion["active"], test_promotion.active)

        # Todo: uncomment this code when get_promotions is implemented
        # Check that the location header was correct
        # response = self.client.get(location)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # new_promotion = response.get_json()
        # self.assertEqual(new_promotion["id"], test_promotion.id)
        # self.assertEqual(new_promotion["name"], test_promotion.name)
        # self.assertEqual(
        #     PromotionType(new_promotion["promotion_type"]),
        #     test_promotion.promotion_type,
        # )
        # self.assertEqual(
        #     _parse_date(new_promotion["start_date"]), test_promotion.start_date
        # )
        # self.assertEqual(
        #     _parse_date(new_promotion["end_date"]), test_promotion.end_date
        # )
        # self.assertEqual(new_promotion["value"], test_promotion.value)
        # self.assertEqual(new_promotion["active"], test_promotion.active)

    # ----------------------------------------------------------
    # TEST DELETE
    # ----------------------------------------------------------
    def test_delete_promotion(self):
        """It should Delete a Promotion"""
        # create a new promotion
        test_promotion = PromotionFactory()
        logging.debug("Test Promotion: %s", test_promotion.serialize())
        response = self.client.post(BASE_URL, json=test_promotion.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # get the promotion id
        new_promotion = response.get_json()
        new_promotion_id = new_promotion["id"]

        response = self.client.delete(f"{BASE_URL}/{new_promotion_id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(len(response.data), 0)
        # Todo: Uncomment this code when read is implemented
        # make sure they are deleted
        # response = self.client.get(f"{BASE_URL}/{new_promotion_id}")
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_non_existing_promotion(self):
        """It should Delete a Promotion even if it doesn't exist"""
        response = self.client.delete(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
