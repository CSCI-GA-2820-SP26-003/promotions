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
from urllib.parse import quote_plus
from wsgi import app
from service.common import status
from service.models import db, Promotion
from service.utils import PromotionType, _parse_date
from .factories import PromotionFactory
from service.models import DataValidationError

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/promotions"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestPromotionService(TestCase):
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

    # def test_index(self):
    # """It should call the home page"""
    # resp = self.client.get("/")
    # self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_index(self):
        """Test the root URL"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.is_json)

        data = resp.get_json()
        self.assertIn("name", data)
        self.assertIn("version", data)
        self.assertIn("resources", data)
        self.assertIn("promotions", data["resources"])

    def test_404_returns_json(self):
        resp = self.client.get("/not_found")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(resp.is_json)

    def test_405_returns_json(self):
        resp = self.client.put("/promotions")
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(resp.is_json)

    ############################################################
    # Utility function to bulk create pets
    ############################################################

    def _create_promotions(self, count: int = 1) -> list:
        """Factory method to create promotions in bulk"""
        promotions = []
        for _ in range(count):
            test_promotion = PromotionFactory()
            response = self.client.post(BASE_URL, json=test_promotion.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test promotion",
            )
            new_promotion = response.get_json()
            test_promotion.id = new_promotion["id"]
            promotions.append(test_promotion)
        return promotions

    # ----------------------------------------------------------
    # TEST LIST
    # ----------------------------------------------------------
    def test_get_pet_list(self):
        """It should Get a list of promotions"""
        self._create_promotions(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

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
        response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_promotion = response.get_json()
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
        response = self.client.get(f"{BASE_URL}/{new_promotion_id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_non_existing_promotion(self):
        """It should Delete a Promotion even if it doesn't exist"""
        response = self.client.delete(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)

    # ----------------------------------------------------------
    # TEST QUERY
    # ----------------------------------------------------------
    def test_query_by_name(self):
        """It should Query Promotions by name"""
        promotions = self._create_promotions(5)
        test_name = promotions[0].name
        name_count = len(
            [promotion for promotion in promotions if promotion.name == test_name]
        )
        response = self.client.get(
            BASE_URL, query_string=f"name={quote_plus(test_name)}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), name_count)
        # check the data just to be sure
        for promotion in data:
            self.assertEqual(promotion["name"], test_name)

    def test_query_promotion_list_by_type(self):
        """It should Query Pets by Promotion Type"""
        promotions = self._create_promotions(10)
        fs_promotions = [
            promotion
            for promotion in promotions
            if promotion.promotion_type == PromotionType.FREE_SHIPPING
        ]

        response = self.client.get(
            BASE_URL, query_string="promotion_type=FREE_SHIPPING"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), len(fs_promotions))
        for promotion in data:
            self.assertEqual(
                promotion["promotion_type"], PromotionType.FREE_SHIPPING.value
            )

    def test_query_by_active(self):
        """It should Query Pets by active status"""
        promotions = self._create_promotions(10)
        active_promotions = [
            promotion for promotion in promotions if promotion.active is True
        ]
        inactive_promotions = [
            promotion for promotion in promotions if promotion.active is False
        ]
        active_count = len(active_promotions)
        inactive_count = len(inactive_promotions)
        logging.debug("Active Promotions [%d] %s", active_count, active_promotions)
        logging.debug(
            "Inactive Promotions [%d] %s", inactive_count, inactive_promotions
        )

        # test for active
        response = self.client.get(BASE_URL, query_string="active=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), active_count)
        # check the data just to be sure
        for promotion in data:
            self.assertEqual(promotion["active"], True)

        # test for inactive
        response = self.client.get(BASE_URL, query_string="active=false")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), inactive_count)
        # check the data just to be sure
        for promotion in data:
            self.assertEqual(promotion["active"], False)

    # ----------------------------------------------------------
    # TEST RETRIEVE
    # ----------------------------------------------------------
    def test_get_promotion_not_found(self):
        """It should return 404 when promotion is not found"""
        response = self.client.get(f"{BASE_URL}/999999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_promotion(self):
        """It should Retrieve a Promotion"""

        test_promo = PromotionFactory()
        response = self.client.post(BASE_URL, json=test_promo.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        promotion_id = response.get_json()["id"]

        # retrieve
        response = self.client.get(f"{BASE_URL}/{promotion_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        self.assertEqual(data["id"], promotion_id)
        self.assertEqual(data["name"], test_promo.name)

    def test_create_promotion_bad_data(self):
        """It should return 400 when bad data is sent"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_promotion_no_json(self):
        """It should return 415 when no JSON is sent"""
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_promotion_invalid_json(self):
        """It should return 400 when invalid JSON is sent"""
        response = self.client.post(
            BASE_URL, data="invalid json", content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_query_invalid_active_value(self):
        """It should handle invalid active query values"""
        response = self.client.get(BASE_URL, query_string="active=notabool")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_serialize_promotion(self):
        """It should serialize a Promotion"""
        promo = PromotionFactory()
        data = promo.serialize()

        self.assertEqual(data["name"], promo.name)
        self.assertEqual(data["promotion_type"], promo.promotion_type.value)
        self.assertEqual(data["value"], promo.value)
        self.assertEqual(data["active"], promo.active)

    def test_update_promotion(self):
        """It should update a Promotion"""
        promo = PromotionFactory()
        promo.create()

        promo.name = "Updated Promotion"
        promo.update()

        found = Promotion.find(promo.id)
        self.assertEqual(found.name, "Updated Promotion")

    def test_deserialize_invalid_type(self):
        """It should raise DataValidationError when deserialize is given wrong type"""
        with self.assertRaises(DataValidationError):
            Promotion().deserialize("this is not a dict")

    def test_query_invalid_promotion_type(self):
        """It should raise KeyError for invalid promotion_type query"""
        with self.assertRaises(KeyError):
            self.client.get(BASE_URL, query_string="promotion_type=INVALID_TYPE")

    def test_find_promotion_not_found(self):
        """It should return None when promotion is not found"""
        result = Promotion.find(999999)
        self.assertIsNone(result)
