#!/bin/sh
export FLASK_APP=./index.py
pipenv run flask --debug run -h 0.0.0.0
# ngrok http 5000 --url=https://primary-dragon-publicly.ngrok-free.app
