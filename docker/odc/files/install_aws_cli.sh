#!/bin/bash
# Install AWS CLI

echo "Installing software"
sudo apt-get update 
sudo apt-get install -y --no-install-recommends awscli ca-certificates
sudo pip3 install boto3 ruamel.yaml
sudo rm -rf /var/lib/apt/lists/*
sudo rm -rf $HOME/.cache/pip

aws configure

