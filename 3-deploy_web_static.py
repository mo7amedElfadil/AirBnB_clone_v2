#!/usr/bin/python3
"""Fabric script that creates and distributes
an archive to my web servers,
using the function deploy"""
from os.path import exists
from fabric.api import local, env, run, put
from datetime import datetime

env.hosts = ["54.144.238.161", "100.25.154.52"]


def do_pack():
    """Packs the web_static files into .tgz file"""
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file = "versions/web_static_{}.tgz".format(date)
    result = local("tar -cvzf {} web_static".format(file))
    if result.failed:
        return None
    return file


def do_deploy(archive_path):
    """Deploys the archive to the web servers
    usage:
    fab -f 2-do_deploy_web_static.py do_deploy:
    archive_path=versions/web_static_20240306225407.tgz
    -i my_ssh_private_key -u ubuntu
    """
    if not archive_path or not exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        target = "/data/web_static/releases/"
        archive_path = archive_path.split("/")[1]
        file = archive_path.split(".")[0]
        print(file)
        run(f"mkdir -p {target}{file}/")
        run(f"if [ -d {target}{file} ]; then rm -rf {target}{file}; fi")
        run(f"if [ -d {target}web_static ]; then \
                rm -rf {target}web_static; fi")
        run(f"tar -xf /tmp/{archive_path} -C {target} \
                && mv {target}web_static {target}{file}/")
        run(f"rm /tmp/{archive_path}")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {target}{file}/ /data/web_static/current")
        run("sudo service nginx restart")
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """Creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    return False
