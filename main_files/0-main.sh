#!/usr/bin/env bash
# transfer and run the script 0-setup_web_static.sh on the server
# This script is used to transfer files from local to remote server
# Usage: 0-transfer_file PATH_TO_FILE IP USERNAME PATH_TO_SSH_KEY


if [ -t 1 ]; then
	COLOR_RED='\033[0;31m'
	COLOR_GREEN='\033[0;32m'
	COLOR_BROWN='\033[0;33m'
	RESET='\033[0m'
fi


function test_result {
	echo -e "${COLOR_BROWN}testing shellcheck of file 0-setup_web_static.sh ${RESET}"
	if shellcheck 0-setup_web_static.sh; then
		echo -e "${COLOR_GREEN}shellcheck success${RESET}"
	else
		echo -e "${COLOR_RED}shellcheck failed${RESET}"
	fi

	echo -e "${COLOR_BROWN}Checking if the folder /data/ is created${RESET}"
	ssh -i $path_to_ssh_key "$USER@$IP" "ls -l /data/"
	echo

	echo -e "${COLOR_BROWN}Checking if the folder /data/web_static/ is created${RESET}"
	ssh -i $path_to_ssh_key "$USER@$IP" "ls -l /data/web_static/"
	echo

	echo -e "${COLOR_BROWN}Checking if the folder /data/web_static/current is created${RESET}"
	ssh -i $path_to_ssh_key "$USER@$IP" "ls -l /data/web_static/current/"
	echo
	
	echo -e "${COLOR_BROWN}Checking content of /data/web_static/current/index.html${RESET}"
	ssh -i $path_to_ssh_key "$USER@$IP" "cat /data/web_static/current/index.html"
	echo

	echo -e "${COLOR_BROWN}Checking if the symbolic link /data/web_static/current is created${RESET}"
	ssh -i $path_to_ssh_key "$USER@$IP" "ls -l /data/web_static/current"
	echo

	echo -e "${COLOR_BROWN}Testing curl -sI $IP ${RESET}"
	if curl -sI "$IP" | grep -i '200 OK'; then
		echo -e "${COLOR_GREEN}root success${RESET}"
	else
		echo -e "${COLOR_RED}root failed${RESET}"
	fi

	echo -e "${COLOR_BROWN}Testing curl -sI $IP/redirect_me ${RESET}"
	if curl -sI "$IP/redirect_me" | grep -i '301 Moved Permanently'; then
		echo -e "${COLOR_GREEN}redirect success${RESET}"
	else
		echo -e "${COLOR_RED}redirect failed${RESET}"
	fi

	echo -e "${COLOR_BROWN}Testing curl -sI $IP/hbnb_static/index.html${RESET}"
	if curl -sI "$IP/hbnb_static/index.html" | grep -i '200 OK' &&
	curl "$IP/hbnb_static/index.html" | grep -i 'Holberton School'; then
		echo -e "${COLOR_GREEN}hbnb success${RESET}"
	else
		echo -e "${COLOR_RED}hbnb failed${RESET}"
	fi
}

# Check if the correct number of arguments is provided
if [ "$#" -lt 1 ] || [ "$#" -gt 3 ]; then
	echo -e "${COLOR_RED}Usage: $0 {1|2} [file_to_transfer] {-y/-n} ${RESET}"
    exit 1
fi
USER=ubuntu
if [ "$1" == 1 ]; then
    IP=$SERVER1
elif [ "$1" == 2 ]; then
    IP=$SERVER2
else
    echo -e "${COLOR_RED}Invalid server selection. Use 1 or 2.${RESET}"
    exit 1
fi
FILE="${2:-0-setup_web_static.sh}"
if [ "$FILE" == "-y" ] || [ "$FILE" == "-n" ]; then
    FILE="0-setup_web_static.sh"
fi
path_to_ssh_key=~/.ssh/id_rsa

echo -e "${COLOR_BROWN}Transferring $FILE to $USER@$IP${RESET}"
if [ ${!#} == "-y" ]; then
	REPLY="y"
else
	echo "Transfer and run the script 0-setup_web_static.sh on the server? (y/n)"
	read -r REPLY
fi
if [ "$REPLY" == "y" ] && scp -o StrictHostKeyChecking=no -i "$path_to_ssh_key" "$FILE" "$USER@$IP":~/ ; then
	echo -e "${COLOR_GREEN}scp success${RESET}"
	installer=$(basename "$FILE")
	ssh -i $path_to_ssh_key "$USER@$IP" "./$installer; rm -f ~/$installer"
	# ssh -o StrictHostKeyChecking=no -i "$path_to_ssh_key" "$USER@$IP" "bash 0-setup_web_static.sh"
	test_result
else
	echo -e "${COLOR_RED}scp failed${RESET}"
fi

