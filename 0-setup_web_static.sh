#!/usr/bin/env bash
# Install nginx and create folders
# Install Nginx if it not already installed
if [ "$(dpkg-query -W -f='${Status}' nginx 2>/dev/null | grep -c "ok installed")" -eq 0 ];
then
	sudo apt-get update -y
	sudo apt-get install nginx -y
else
	echo "Nginx is already installed"
fi
# Create the following folders if they don’t already exist:
# /data/
# /data/web_static/
# /data/web_static/releases/
# /data/web_static/shared/
# /data/web_static/releases/test/
directories=(
	"/data/" 
	"/data/web_static/"
	"/data/web_static/releases/"
	"/data/web_static/shared/"
	"/data/web_static/releases/test/"
)
for i in "${directories[@]}"
do
	if [ ! -d "$i" ];
	then
		sudo mkdir "$i"
	fi
done	


# Create a fake HTML file /data/web_static/releases/test/index.html (with simple content, to test your Nginx configuration)
echo "
<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
	Holberton School
  </body>
</html>	
" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder. If the symbolic link already exists, it should be deleted and recreated every time the script is ran.
if [ -L /data/web_static/current ];
then
	sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group (you can assume this user and group exist). This should be recursive; everything inside should be created/owned by this user/group.
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static (ex: https://mydomainname.tech/hbnb_static). Don’t forget to restart Nginx after updating the configuration:


my_setup="server {
	add_header X-Served-By $HOSTNAME;
	listen 80 default_server;
	listen [::]:80 default_server;
	root /var/www/html;
	index index.html;
	server_name _;
	location / {
		try_files \$uri \$uri/ =404;
	}
	location /redirect_me {
		return 301 https://www.youtube.com/watch?v=dQw4w9WgXcQ;
	}

	location /hbnb_static/ {
		alias /data/web_static/current/;
		index index.html;
	}
	error_page 404 /404.html;
	location = /404.html {
		internal;
	}
}" 
	echo -e "$my_setup" | sudo tee /etc/nginx/sites-available/default > /dev/null

	sudo service nginx restart
