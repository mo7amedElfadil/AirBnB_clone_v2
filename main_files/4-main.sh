#!/usr/bin/env bash
FILE="100-clean_web_static.py"
COMMAND="do_clean"
SSH_KEY="$HOME/.ssh/id_rsa"
NUM="${1:-1}"
USER="ubuntu"
fab -f $FILE $COMMAND:number=$NUM -i $SSH_KEY -u $USER > /dev/null 2>&1
