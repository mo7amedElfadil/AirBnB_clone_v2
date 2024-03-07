#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive
from the contents of the web_static folder of
AirBnB Clone repo
"""
from os.path import basename, exists, splitext
from fabric.api import local, env, run, put, cd
from datetime import datetime

env.hosts = ["54.144.238.161", "100.25.154.52"]
env.user = "ubuntu"


def do_pack():
    """Packs the web_static files into .tgz file"""
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file = f"versions/web_static_{date}.tgz"
    print("Packing web_static to {}".format(file))
    if local(f"tar -cvzf {file} web_static").succeeded:
        return file
    return None


def do_deploy(archive_path):
    """Deploys the archive to the web servers
    usage:
    fab -f 2-do_deploy_web_static.py do_deploy:
    archive_path=versions/web_static_20240306225407.tgz
    -i my_ssh_private_key -u ubuntu
    """
    try:
        if not exists(archive_path):
            return False

        target = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        archive_path = basename(archive_path)
        file, _ = splitext(archive_path)

        with cd(target):
            run(f"mkdir -p {file}")
            run(f"tar -xzf /tmp/{archive_path} -C {file}")
            run(f"mv {file}/web_static/* {file} && rm -rf {file}/web_static")

        run(f"rm /tmp/{archive_path}")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {target}{file} /data/web_static/current")

        print("New version deployed!")

    except Exception:
        return False

    return True
