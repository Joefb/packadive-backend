#!/bin/bash
set -e
export FLASK_APP=wsgi.py
export FLASK_CONFIG=ProductionConfig
flask db upgrade
exec gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app('ProductionConfig')"
