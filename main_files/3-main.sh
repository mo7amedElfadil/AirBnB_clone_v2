#!/usr/bin/env bash
FILE="3-deploy_web_static.py"
COMMAND="deploy"
SSH_KEY="$HOME/.ssh/id_rsa"
ARCHIVE=$(ls -t "versions"/*.tgz | head -n1)
USER="ubuntu"
fab -f $FILE $COMMAND -i $SSH_KEY -u $USER
