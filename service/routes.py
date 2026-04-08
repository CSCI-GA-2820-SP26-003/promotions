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
Promotions Service

This service implements a REST API that allows you to Create, Read,
and Delete Promotions
"""

from flask import request, abort
from flask import current_app as app  # Import Flask application
from flask_restx import Namespace, Resource, fields
from service import api
from service.models import Promotion
from service.common import status  # HTTP Status Codes
from service.utils import PromotionType

promotions_ns = Namespace("promotions", description="Promotion operations")
root_ns = Namespace("", description="Root operations")

######################################################################
# Namespace
######################################################################


######################################################################
# Model Definition for Swagger
######################################################################

promotion_model = promotions_ns.model(
    "Promotion",
    {
        "id": fields.Integer(readOnly=True, description="The unique id of a promotion"),
        "name": fields.String(required=True, description="The name of the promotion"),
        "description": fields.String(description="The description of the promotion"),
        "promotion_type": fields.Integer(description="The type of promotion"),
        "start_date": fields.String(description="The start date"),
        "end_date": fields.String(description="The end date"),
        "value": fields.Integer(description="The promotion value"),
        "active": fields.Boolean(description="Whether the promotion is active"),
    },
)
######################################################################
# Add Namespace
######################################################################
api.add_namespace(root_ns, path="")
api.add_namespace(promotions_ns, path="/promotions")


######################################################################
# HEALTH ENDPOINT
######################################################################
@root_ns.route("/health")
class HealthResource(Resource):
    """Health check endpoint"""

    def get(self):
        """
        Health check endpoint
        Returns the health status of the service
        """
        app.logger.info("Health check requested")
        return {"status": "healthy"}, status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@root_ns.route("/")
class RootResource(Resource):
    """Root resource"""

    def get(self):
        """Root URL response"""
        return {
            "name": "Promotions REST API Service",
            "version": "1.0",
            "paths": "/promotions",
            "ui": "/ui",
        }, status.HTTP_200_OK


@app.route("/ui")
def ui_index():
    return app.send_static_file("index.html")


######################################################################
# Utility Functions
######################################################################
def check_content_type(content_type: str):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )


def str_to_bool(value):
    """Convert query parameter to boolean"""
    if value is None:
        return None

    value = value.lower()

    if value in ["true", "1", "yes", "y"]:
        return True

    if value in ["false", "0", "no", "n"]:
        return False

    return None


######################################################################
# LIST ALL PROMOTIONS / CREATE PROMOTION
######################################################################
@promotions_ns.route("")
@promotions_ns.route("/")
class PromotionCollection(Resource):
    """
    Handles all interactions with collections of Promotions
    """

    ##################################################################
    # LIST ALL PROMOTIONS
    ##################################################################
    @promotions_ns.marshal_list_with(promotion_model)
    def get(self):
        """
        Returns all Promotions
        """
        app.logger.info("Request for promotion list")

        name = request.args.get("name")
        promotion_type = request.args.get("promotion_type")
        active = request.args.get("active")
        value = request.args.get("value")

        # Query by name
        if name:
            promotions = Promotion.find_by_name(name)

        # Query by promotion type
        elif promotion_type:
            promotions = Promotion.find_by_promotion_type(
                PromotionType[promotion_type.upper()]
            )

        # Query by active status
        elif active is not None:
            active_value = str_to_bool(active)

            # invalid active values should return empty list
            if active_value is None:
                promotions = []
            else:
                promotions = Promotion.find_by_active(active_value)

        # Query by promotion value
        elif value is not None:
            if value == "":
                promotions = []
            else:
                try:
                    promotions = Promotion.find_by_value(int(value))
                except ValueError:
                    promotions = []

        # Return all promotions
        else:
            promotions = Promotion.all()

        results = [promotion.serialize() for promotion in promotions]
        return results, status.HTTP_200_OK

    ##################################################################
    # CREATE A NEW PROMOTION
    ##################################################################
    @promotions_ns.expect(promotion_model)
    @promotions_ns.marshal_with(promotion_model)
    def post(self):
        """
        Creates a Promotion
        """
        app.logger.info("Request to create a promotion")

        check_content_type("application/json")

        promotion = Promotion()
        data = request.get_json()

        promotion.deserialize(data)
        promotion.create()

        location_url = f"{request.host_url.rstrip('/')}/promotions/{promotion.id}"

        return (
            promotion.serialize(),
            status.HTTP_201_CREATED,
            {"Location": location_url},
        )


######################################################################
# RETRIEVE / UPDATE / DELETE A SINGLE PROMOTION
######################################################################
@promotions_ns.route("/<int:promotion_id>")
@promotions_ns.param("promotion_id", "The Promotion identifier")
class PromotionResource(Resource):
    """
    Handles operations on a single Promotion
    """

    ##################################################################
    # RETRIEVE A PROMOTION
    ##################################################################
    @promotions_ns.marshal_with(promotion_model)
    def get(self, promotion_id):
        """
        Retrieve a single Promotion
        """
        app.logger.info("Request to retrieve promotion with id [%s]", promotion_id)

        promotion = Promotion.find(promotion_id)

        if not promotion:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Promotion with id '{promotion_id}' was not found.",
            )

        return promotion.serialize(), status.HTTP_200_OK

    ##################################################################
    # UPDATE A PROMOTION
    ##################################################################
    @promotions_ns.expect(promotion_model)
    @promotions_ns.marshal_with(promotion_model)
    def put(self, promotion_id):
        """
        Update a Promotion
        """
        app.logger.info("Request to update promotion with id [%s]", promotion_id)

        check_content_type("application/json")

        promotion = Promotion.find(promotion_id)

        if not promotion:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Promotion with id '{promotion_id}' was not found.",
            )

        data = request.get_json()

        promotion.deserialize(data)
        promotion.id = promotion_id
        promotion.update()

        return promotion.serialize(), status.HTTP_200_OK

    ##################################################################
    # DELETE A PROMOTION
    ##################################################################
    def delete(self, promotion_id):
        """
        Delete a Promotion
        """
        app.logger.info("Request to delete promotion with id [%s]", promotion_id)

        promotion = Promotion.find(promotion_id)

        if promotion:
            promotion.delete()

        return "", status.HTTP_204_NO_CONTENT


######################################################################
# ACTIVATE A PROMOTION
######################################################################
@promotions_ns.route("/<int:promotion_id>/activate")
@promotions_ns.param("promotion_id", "The Promotion identifier")
class ActivatePromotion(Resource):
    """Activate a Promotion"""

    @promotions_ns.marshal_with(promotion_model)
    def put(self, promotion_id):
        """Activate a promotion"""
        app.logger.info("Request to activate promotion with id [%s]", promotion_id)

        promotion = Promotion.find(promotion_id)

        if not promotion:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Promotion with id '{promotion_id}' was not found.",
            )

        promotion.active = True
        promotion.update()

        return promotion.serialize(), status.HTTP_200_OK


######################################################################
# DEACTIVATE A PROMOTION
######################################################################
@promotions_ns.route("/<int:promotion_id>/deactivate")
@promotions_ns.param("promotion_id", "The Promotion identifier")
class DeactivatePromotion(Resource):
    """Deactivate a Promotion"""

    @promotions_ns.marshal_with(promotion_model)
    def put(self, promotion_id):
        """Deactivate a promotion"""
        app.logger.info("Request to deactivate promotion with id [%s]", promotion_id)

        promotion = Promotion.find(promotion_id)
        if not promotion:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Promotion with id '{promotion_id}' was not found.",
            )

        promotion.active = False
        promotion.update()

        return promotion.serialize(), status.HTTP_200_OK
