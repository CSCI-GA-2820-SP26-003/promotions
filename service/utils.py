from enum import Enum
from datetime import date
from email.utils import parsedate_to_datetime


class PromotionType(Enum):
    """
    Enum class describing promotion types
    Indicates which type of promotion its value corresponds to
    """

    PERCENT_OFF = 1  # valid Value: 0-100
    BUY_N_GET_ONE = 2  # valid Value: int >= 1
    FIXED_DISCOUNT = 3  # valid Value: int > 0 (in USD)
    FREE_SHIPPING = 4  # valid Value: fixed or minimum purchase amount (tbd)
    PAYBACK_PERCENT = 5  # valid Value: 1-100

def validate_promotion_value(promotion_type, value):
    """Validate value based on promotion type"""

    if value < 0:
        raise ValueError("value cannot be negative")

    if promotion_type == PromotionType.PERCENT_OFF:
        if value < 1 or value > 100:
            raise ValueError("value is invalid for PERCENT_OFF")

    elif promotion_type == PromotionType.PAYBACK_PERCENT:
        if value < 1 or value > 100:
            raise ValueError("value is invalid for PAYBACK_PERCENT")

    elif promotion_type in (PromotionType.BUY_N_GET_ONE, PromotionType.FIXED_DISCOUNT):
        if value <= 0:
            raise ValueError("value is invalid for BUY_N_GET_ONE or FIXED_DISCOUNT")

def _parse_date(value):
    if value is None:
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError:
            pass
        try:
            return parsedate_to_datetime(value).date()
        except Exception as error:
            raise ValueError("Invalid date string: " + value) from error
    raise TypeError("Invalid date type: " + str(type(value)))
