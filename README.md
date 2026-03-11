# NYU DevOps Project : Promotions

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-lightgrey.svg)](https://flask.palletsprojects.com/)
![Build Status](https://github.com/CSCI-GA-2820-SP26-003/promotions/actions/workflows/workflow.yml/badge.svg)

# Promotions Service

The Promotions Service is a RESTful web service for creating and managing retail promotions. It stores promotion metadata in a PostgreSQL database and exposes endpoints to create, retrieve, list, filter, and delete promotions. Promotions support multiple business rules such as percentage discounts, fixed discounts, free shipping, and buy-n-get-one offers.

## Overview

This project is built with Flask and Flask-SQLAlchemy and follows a service-oriented layout with separate modules for configuration, models, routes, utilities, and tests.

Each promotion includes:

- `id`: unique identifier
- `name`: name of the promotion
- `promotion_type`: one of the supported promotion categories: `PERCENT_OFF`, `BUY_N_GET_ONE`, `FIXED_DISCOUNT`, `FREE_SHIPPING`
- `start_date`: date the promotion becomes valid
- `end_date`: date the promotion expires
- `value`: numeric value associated with the promotion type
- `active`: boolean status indicating whether the promotion is currently active

## Project Structure

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
pyproject.toml      - Poetry list of Python libraries required by your code

service/                   - service python package
├── __init__.py            - package initializer
├── config.py              - configuration parameters
├── models.py              - module with business models
├── routes.py              - module with service routes
├── utils.py               - utilities for models.py and routes.py
└── common                 - common code package
    ├── cli_commands.py    - Flask command to recreate all tables
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/                     - test cases package
├── __init__.py            - package initializer
├── factories.py           - Factory for testing with fake objects
├── test_cli_commands.py   - test suite for the CLI
├── test_models.py         - test suite for business models
└── test_routes.py         - test suite for service routes
```

## Tech Stack

- Python 3.12
- Flask 3.1
- Flask-SQLAlchemy 3.1
- PostgreSQL with `psycopg`


## API Endpoints

| Method   | Endpoint                     | Description                    |
| -------- | ---------------------------- | ------------------------------ |
| `GET`    | `/`                          | Root |
| `POST`   | `/promotions`                | Create a new promotion         |
| `GET`    | `/promotions`                | List all promotions            |
| `GET`    | `/promotions/<promotion_id>` | Retrieve a promotion by ID     |
| `PUT`    | `/promotions/<promotion_id>` | Update a promotion by ID       |
| `DELETE` | `/promotions/<promotion_id>` | Delete a promotion by ID       |



### Query parameters

The list endpoint supports filtering with query parameters:

- `id`
- `name`
- `promotion_type`
- `active`


## Testing

Run the full test suite with:

```bash
make test
```


## Authors

- Jason Chen
- Gustave Martinez
- Amy Kim
- Esha Pandey
- Curie Yoon

## License

Copyright (c) 2016, 2025 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
