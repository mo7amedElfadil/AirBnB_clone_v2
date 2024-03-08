# This is a manifest file for the web_static deployment
# It will install nginx, create the necessary directories and files, and configure the server to serve the content

# install and configure nginx server
package { 'nginx':
  ensure   => 'installed',
  provider => 'apt',
}

# create the necessary directories
$dir_names = ['/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/shared', '/data/web_static/releases/test']
# create the necessary directories
-> file { $dir_names:
  ensure  => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  require => Package['nginx'],
}

# create the necessary files
-> file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content =>  "
<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
	Holberton School
  </body>
</html>	
",
  require => File['/data/web_static/releases/test'],
}

-> file { '/data/web_static/current':
  ensure  => 'link',
  target  => '/data/web_static/releases/test',
  require => File['/data/web_static/releases/test/index.html'],
}

-> file { '/etc/nginx/sites-available/default':
    ensure  => file,
    content => "server {
	add_header X-Served-By ${hostname};
	listen 80 default_server;
	listen [::]:80 default_server;
	root /var/www/html;
	index index.html;
	server_name _;
	location / {
		try_files \$uri \$uri/ =404;
	}

	location /hbnb_static/ {
		alias /data/web_static/current/;
	}
	location /redirect_me {
		return 301 https://www.youtube.com/watch?v=dQw4w9WgXcQ;
	}
	error_page 404 /404.html;
	location = /404.html {
		internal;
	}
}",
    require => Package['nginx'],
}

# restart the server
-> exec {'nginx restart':
  command   => '/usr/sbin/service nginx restart',
  subscribe => File['/etc/nginx/sites-available/default'],
}
