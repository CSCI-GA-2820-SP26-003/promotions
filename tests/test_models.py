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
Test cases for Promotion Model
"""

# pylint: disable=duplicate-code
import os
import logging
from unittest import TestCase
from wsgi import app
from service.models import Promotion, DataValidationError, db
from service.utils import PromotionType
from .factories import PromotionFactory
from datetime import date, timedelta

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  Promotion   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestPromotion(TestCase):
    """Test Cases for Promotion Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Promotion).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_example_replace_this(self):
        """It should create a Promotion"""
        # Todo: Remove this test case example
        resource = PromotionFactory()
        resource.create()
        self.assertIsNotNone(resource.id)
        found = Promotion.all()
        self.assertEqual(len(found), 1)
        data = Promotion.find(resource.id)
        self.assertEqual(data.name, resource.name)

    # Todo: Add your test cases here...
    def test_create_a_promotion(self):
        """It should Create a promotion and assert that it exists"""
        promotion = Promotion(
            id=32467,
            name="Free Shipping for New Members",
            promotion_type=PromotionType.FREE_SHIPPING,
            start_date=date(2026, 1, 19),
            end_date=date(2026, 2, 18),
            value=10,
            active=False,
        )
        # self.assertEqual(str(promotion), "<Promotion Fido id=[None]>")
        self.assertTrue(promotion is not None)
        self.assertEqual(promotion.id, 32467)
        self.assertEqual(promotion.name, "Free Shipping for New Members")
        self.assertEqual(promotion.promotion_type, PromotionType.FREE_SHIPPING)
        self.assertEqual(promotion.start_date, date(2026, 1, 19))
        self.assertEqual(promotion.end_date, date(2026, 2, 18))
        self.assertEqual(promotion.value, 10)
        self.assertEqual(promotion.active, False)

<<<<<<< HEAD
    def test_delete_a_promotion(self):
        """It should Delete a promotion"""
        promotion = PromotionFactory()
        promotion.create()
        self.assertEqual(len(Promotion.all()), 1)
        # delete the pet and make sure it isn't in the database
        promotion.delete()
        self.assertEqual(len(Promotion.all()), 0)
=======
    def test_list_promotions(self):
        """It should list all Promotions in the database"""
        promotions = Promotion.all()
        self.assertEqual(promotions, [])
        for _ in range(5):
            promotion = PromotionFactory()
            promotion.create()
        # See if we get back 5 promotions
        promotions = Promotion.all()
        self.assertEqual(len(promotions), 5)


######################################################################
#  Q U E R Y   T E S T   C A S E S
######################################################################
class TestModelQueries(TestPromotion):
    """Promotion Model Query Tests"""

    def test_find_by_name(self):
        """It should Find a Promotion by Name"""
        promotions = PromotionFactory.create_batch(10)
        for promotion in promotions:
            promotion.create()
        name = promotions[0].name
        count = len([promotion for promotion in promotions if promotion.name == name])
        found = Promotion.find_by_name(name)
        self.assertEqual(found.count(), count)
        for promotion in found:
            self.assertEqual(promotion.name, name)

    def test_find_by_active(self):
        """It should Find a Promotion by Active status"""
        today = date.today()
        active_promotions = []
        inactive_promotions = []

        for i in range(10):
            promotion = PromotionFactory()
            promotion.id = None
            if i % 2 == 0:
                # active: start <= today <= end
                promotion.start_date = today - timedelta(days=5)
                promotion.end_date = today + timedelta(days=5)
                active_promotions.append(promotion)
            else:
                # inactive: ended in the past
                promotion.start_date = today - timedelta(days=10)
                promotion.end_date = today - timedelta(days=1)
                inactive_promotions.append(promotion)
            promotion.create()

        found_active = Promotion.find_by_active(True)
        self.assertEqual(found_active.count(), len(active_promotions))
        for promotion in found_active:
            self.assertEqual(promotion.active, True)

        found_inactive = Promotion.find_by_active(False)
        self.assertEqual(found_inactive.count(), len(inactive_promotions))
        for promotion in found_inactive:
            self.assertEqual(promotion.active, False)

    def test_find_by_type(self):
        """It should Find a Promotion by Promotion type"""
        promotions = []
        for i in range(10):
            promotion = PromotionFactory()
            promotion.id = None
            promotion.promotion_type = (
                PromotionType.FREE_SHIPPING if i % 2 == 0 else PromotionType.PERCENT_OFF
            )
            promotion.create()
            promotions.append(promotion)

        promotion_type = promotions[0].promotion_type
        count = len(
            [
                promotion
                for promotion in promotions
                if promotion.promotion_type == promotion_type
            ]
        )

        found = Promotion.find_by_promotion_type(promotion_type)
        self.assertEqual(found.count(), count)
        for promotion in found:
            self.assertEqual(promotion.promotion_type, promotion_type)
>>>>>>> origin/master
