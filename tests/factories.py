"""
Test Factory to make fake objects for testing
"""

import factory
from factory import fuzzy
from service.models import Promotion
from service.utils import PromotionType
from datetime import date, timedelta


class PromotionFactory(factory.Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Promotion

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    promotion_type = fuzzy.FuzzyChoice(list(PromotionType))
    value = fuzzy.FuzzyInteger(1, 100)
    # Temporarily only creating expired promotions
    start_date = fuzzy.FuzzyDate(date(2020, 1, 1), date.today() - timedelta(days=1))
    end_date = fuzzy.FuzzyDate(date(2020, 1, 1), date.today() - timedelta(days=1))
    # Todo: uncomment this code when active status auto-detection is implemented
    # active = fuzzy.FuzzyChoice(choices=[True, False])
    active = False
