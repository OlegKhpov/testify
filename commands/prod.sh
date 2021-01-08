#!/bin/bash

gunicorn -w ${WORKERS} -b 0:${PORT} app.wsgi:application
