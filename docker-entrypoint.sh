#!/bin/bash

alembic upgrade head

exec python src/main.py --host 0.0.0.0 --port 8000
