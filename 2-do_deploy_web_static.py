#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['54.89.109.87', '100.25.190.21']

def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if not exists(archive_path):
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension>
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(file_n))

        # Move the contents of the archive to the final location
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))

        # Remove the now empty directory
        run('rm -rf {}{}/web_static'.format(path, no_ext))

        # Delete the symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))

        print("New version deployed!")
        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False