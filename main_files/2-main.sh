#!/usr/bin/env bash

FILE="2-do_deploy_web_static.py"
COMMAND="do_deploy"
SSH_KEY="$HOME/.ssh/id_rsa"
ARCHIVE=$(ls -t "versions"/*.tgz | head -n1)
USER="ubuntu"
fab -f $FILE $COMMAND:archive_path=$ARCHIVE -i $SSH_KEY -u $USER
