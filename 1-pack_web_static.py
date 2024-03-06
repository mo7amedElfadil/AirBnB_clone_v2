#!/home/mo7amed/alx_se/myAirBnb_v2/AirBnB_clone_v2/venv/bin/python3.8
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
    file = "versions/web_static_{}.tgz".format(date)
    result = local("tar -cvzf {} web_static".format(file))
    if result.failed:
        return None
    return file
