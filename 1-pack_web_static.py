#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive
from the contents of the web_static folder of
AirBnB Clone repo
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """Packs the web_static files into .tgz file"""
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file = f"versions/web_static_{date}.tgz"
    print("Packing web_static to {}".format(file))
    if local(f"tar -cvzf {file} web_static").succeeded:
        return file
    return None
