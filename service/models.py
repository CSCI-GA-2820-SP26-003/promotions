"""
Models for Promotion

All of the models are stored in this module
"""

import logging
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from .utils import PromotionType, _parse_date


logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Promotion(db.Model):
    """
    Class that represents a Promotion
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    promotion_type = db.Column(db.Enum(PromotionType))
    start_date = db.Column(db.Date())
    # <class 'datetime.date'>
    end_date = db.Column(db.Date())
    value = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True, nullable=False)

    # Todo: Place the rest of your schema here...

    def __repr__(self):
        return ""

    #   return f"<Promotion id=[{self.id}], name=[{self.name}], type=[{self.promotion_type}], start_date=[{self.start_date}], end_date=[{self.end_date}], value=[{self.value}], active=[{self.active}]>"

    def create(self):
        """
        Creates a Promotion to the database
        """
        self.active = (
            True
            if (date.today() >= self.start_date and date.today() <= self.end_date)
            else False
        )
        logger.info("Creating Promotion")
        logger.info(f"ID={self.id}")
        logger.info(f"name={self.name}")
        logger.info(f"promotion type={PromotionType(self.promotion_type).name}")
        logger.info(f"value={self.value}")
        logger.info(f"start_date={self.start_date.strftime('%b-%d-%Y')}")
        logger.info(f"end_date={self.end_date.strftime('%b-%d-%Y')}")
        logger.info(f"active={self.active}")

        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error creating record: %s", self)
            raise DataValidationError(e) from e

    def update(self):
        """
        Updates a Promotion to the database
        """
        logger.info("Saving %s", self.name)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error updating record: %s", self)
            raise DataValidationError(e) from e

    def delete(self):
        """Removes a Promotion from the data store"""
        logger.info("Deleting %s", self.name)
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error deleting record: %s", self)
            raise DataValidationError(e) from e

    def serialize(self):
        """Serializes a Promotion into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "promotion_type": self.promotion_type.value,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "value": self.value,
            "active": self.active,
        }

    def deserialize(self, data):
        """
        Deserializes a Promotion from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """

        try:
            self.id = data["id"]
            self.name = data["name"]
            self.promotion_type = PromotionType(data["promotion_type"])
            self.start_date = _parse_date(data["start_date"])
            self.end_date = _parse_date(data["end_date"])
            self.value = data["value"]
            self.active = data["active"]
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid Promotion: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Promotion: body of request contained bad or no data "
                + str(error)
            ) from error
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def all(cls):
        """Returns all of the Promotions in the database"""
        logger.info("Processing all Promotions")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a Promotion by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.session.get(cls, by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Promotions with the given name

        Args:
            name (string): the name of the Promotions you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
