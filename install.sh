#!/bin/bash

#Install System-Level Dependencies
sudo apt install -y python3 python3-venv ffmpeg libportaudio2 libportaudiocpp0 portaudio19-dev

#Create Virtual Environment
python3 -m venv venv
source ./venv/bin/activate

#Install Python-Level Dependencies
pip install -r ./requirements.txt

# Install node and npm by way of nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install node
cd server && npm i && cd ..
