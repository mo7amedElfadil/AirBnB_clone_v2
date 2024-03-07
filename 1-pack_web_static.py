#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive
from the contents of the web_static folder of
AirBnB Clone repo
"""
from fabric.api import local, task
from datetime import datetime
from os.path import getsize


@task
def do_pack():
    """Packs the web_static files into .tgz file"""
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file = "versions/web_static_{}.tgz".format(date)
    print("Packing web_static to {}".format(file))
    local("mkdir -p versions")
    if local("tar -cvzf {} web_static".format(file)).succeeded:
        print("web_static packed: {} -> {}Bytes".format(file, getsize(file)))
        return file
    return None
