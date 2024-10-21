#!/bin/bash

export FLASK_APP=./index.py

echo 'Starting ngrok ...'
osascript -e 'tell application "Terminal" to do script "ngrok http 5000 --url=https://primary-dragon-publicly.ngrok-free.app"'

echo "Starting server ..."
pipenv run flask --debug run -h 0.0.0.0
