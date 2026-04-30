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

"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up the logging
and SQL database
"""

import sys
from flask import Flask
from flask_restx import Api
from service import config
from service.common import log_handlers

############################################################
# Initialize the Flask instance
############################################################
api = Api(
    title="Promotions API",
    version="1.0.0",
    description="Promotions service API",
    doc="/apidocs",
    prefix="/api",
)


def api_root():
    """Root URL response for Flask-RESTX"""
    return {
        "name": "Promotions REST API Service",
        "version": "1.0",
        "resources": {"promotions": "/api/promotions"},
    }, 200


api.render_root = api_root


def create_app():
    """Initialize the core application."""
    # Create Flask application
    app = Flask(__name__, static_folder="static", static_url_path="/static")
    app.config.from_object(config)

    @app.errorhandler(404)
    def not_found(_error):
        """Return JSON for 404 errors"""
        return {"message": "Not Found"}, 404

    # Initialize Flask-RESTX
    api.init_app(app)

    from service.models import db  # pylint: disable=import-outside-toplevel

    db.init_app(app)

    with app.app_context():
        # Dependencies require we import the routes AFTER the Flask app is created
        # pylint: disable=wrong-import-position, wrong-import-order, unused-import
        from service import routes  # pylint: disable=import-outside-toplevel
        from service import models  # pylint: disable=import-outside-toplevel

        # pylint: disable=import-outside-toplevel
        from service.common.cli_commands import (
            db_create,
        )

        app.cli.command("db-create")(db_create)

        try:
            db.create_all()
        except Exception as error:  # pylint: disable=broad-except  # pragma: no cover
            app.logger.warning(
                "Database initialization failed: %s (continuing with degraded functionality)",
                error,
            )  # pragma: no cover

        # Set up logging for production
        log_handlers.init_logging(app, "gunicorn.error")

        app.logger.info(70 * "*")
        app.logger.info("  S E R V I C E   R U N N I N G  ".center(70, "*"))
        app.logger.info(70 * "*")

        app.logger.info("Service initialized!")

        return app
