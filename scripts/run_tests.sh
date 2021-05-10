#!/bin/bash

coverage run --source='bicycleparking/' manage.py test --no-input
coverage html
coverage report --show-missing
