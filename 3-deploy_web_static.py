#!/usr/bin/python3
"""
Fabric script that creates and distributes
an archive to my web servers,
using the function deploy
"""
from os.path import basename, exists, splitext
from fabric.api import local, env, run, put, runs_once, cd, task
from datetime import datetime
from os.path import getsize

env.hosts = ["54.144.238.161", "100.25.154.52"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def test(cmd):
    """Tests the command and returns True if successful"""
    if cmd.return_code == 0:
        return False
    return True


@runs_once
def do_pack():
    """Packs the web_static files into .tgz file"""
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file = "versions/web_static_{}.tgz".format(date)
    print("Packing web_static to {}".format(file))
    if test(local("mkdir -p versions")):
        return None
    if not test(local("tar -cvzf {} web_static".format(file), capture=True)):
        print("web_static packed: {} -> {}Bytes".format(file, getsize(file)))
        return file
    return None


@task
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
        if test(put(archive_path, "/tmp/")):
            return False
        archive_path = basename(archive_path)
        file, _ = splitext(archive_path)

        with cd(target):
            if test(run("mkdir -p {}".format(file))):
                return False
            if test(run("tar -xzf /tmp/{} -C {}"
                        .format(archive_path, file))):
                return False
            if test(run("mv {}/web_static/* {} && rm -rf {}/web_static"
                        .format(file, file, file))):
                return False

        if test(run("rm /tmp/{}".format(archive_path))):
            return False
        if test(run("rm -rf /data/web_static/current")):
            return False
        if test(run("ln -s {}{}/ /data/web_static/current"
                    .format(target, file))):
            return False

        print("New version deployed!")

    except Exception:
        return False

    return True


@task(default=True)
def deploy():
    """ Creates and distributes an archive to the web servers
        usage: fab -f 3-deploy_web_static.py deploy
    """
    try:
        archive_path = do_pack()
        if archive_path is None:
            return False
        return do_deploy(archive_path)
    except Exception:
        return False
