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
    file = f"versions/web_static_{date}.tgz"
    print(f"Packing web_static to {file}")
    local("mkdir -p versions")
    if local(f"tar -cvzf {file} web_static").succeeded:
        print(f"web_static packed: {file} -> {getsize(file)}Bytes")
        return file
    return None
