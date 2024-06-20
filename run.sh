#!/bin/bash

# cd ./express/ && npm run start & cd .. &&
cd express && npm run start &
source ./venv/bin/activate
python3 ./audio_controller/server.py
