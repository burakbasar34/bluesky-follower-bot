#!/bin/bash
source /bluesky-bot/venv/bin/activate
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000 main:app