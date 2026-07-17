#!/bin/bash
set -e
python planadive.py
exec gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app('ProductionConfig')"
