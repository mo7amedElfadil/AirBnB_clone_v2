#!/usr/bin/env bash
# transfer and run the script 0-setup_web_static.sh on the server
# This script is used to transfer files from local to remote server
# Usage: 0-transfer_file PATH_TO_FILE IP USERNAME PATH_TO_SSH_KEY
# Check if the correct number of arguments is provided
if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
    echo "Usage: $0 {1|2} [file_to_transfer]"
    exit 1
fi
USER=ubuntu
if [ "$1" == 1 ]; then
    IP=$SERVER1
elif [ "$1" == 2 ]; then
    IP=$SERVER2
else
    echo "Invalid server selection. Use 1 or 2."
    exit 1
fi
FILE="${2:-0-setup_web_static.sh}"
path_to_ssh_key=~/.ssh/id_rsa

echo "Transferring $FILE to $USER@$IP"
if  scp -o StrictHostKeyChecking=no -i "$path_to_ssh_key" "$FILE" "$USER@$IP":~/ ; then
	echo "scp success"
	installer=$(basename $FILE)
	ssh -i $path_to_ssh_key "$USER@$IP" "./$installer; rm -f ~/$installer"
	# ssh -o StrictHostKeyChecking=no -i "$path_to_ssh_key" "$USER@$IP" "bash 0-setup_web_static.sh"

	echo "Checking if the folder /data/ is created"
	ssh -i $path_to_ssh_key "$USER@$IP" "ls -l /data/"
	echo

	echo "Checking if the folder /data/web_static/ is created"
	ssh -i $path_to_ssh_key "$USER@$IP" "ls -l /data/web_static/"
	echo

	echo "Checking if the folder /data/web_static/current is created"
	ssh -i $path_to_ssh_key "$USER@$IP" "ls -l /data/web_static/current/"
	echo
	
	echo "Checking content of /data/web_static/current/index.html"
	ssh -i $path_to_ssh_key "$USER@$IP" "cat /data/web_static/current/index.html"
	echo

else
	echo "scp failed"
fi

