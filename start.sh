#!/bin/bash
set -e

cd /app

python db_init.py

exec uvicorn main:socket_app --host 0.0.0.0 --port 3001