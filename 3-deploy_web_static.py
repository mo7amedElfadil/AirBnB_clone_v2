#!/usr/bin/python3
"""Fabric script that creates and distributes
an archive to my web servers,
using the function deploy"""
from os.path import basename, exists, splitext
from fabric.api import local, env, run, put, runs_once, cd, task
from datetime import datetime
from os.path import getsize

env.hosts = ["54.144.238.161", "100.25.154.52"]
env.user = "ubuntu"


@runs_once
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


@task()
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


@task(default=True)
def deploy():
    """Creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    return False
