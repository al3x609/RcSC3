#!/usr/bin/env python
# -*- coding: utf-8 -*-

import docker


def run_nclient(listen_port, cmd, username, user, group, home):
    imageName = "al3x609/nvnc:latest"
    containerName = "nvnc-" + username

    nclient = docker.from_env()
    nclient.containers.run(
        detach=True,
        command=cmd,
        image=imageName,
        runtime="nvidia",
        auto_remove=True,
        name=containerName,
        hostname=containerName,
        working_dir="/opt/noVNC",
        ports={'6080/tcp': listen_port},
        user=str(user) + ":" + str(group),
        environment=[
            "VGL_LOGO=1",
            "USER=" + username,
            "LIBGL_DEBUG=verbose",
            "NVIDIA_VISIBLE_DEVICES=all",
            "NVIDIA_DRIVER_CAPABILITIES=all",
            "QT_XKB_CONFIG_ROOT=/usr/share/X11/xkb"
        ],
        volumes={
            home: {'bind': home, 'mode': 'ro'},
            '/etc/group': {'bind': '/etc/group', 'mode': 'ro'},
            '/etc/passwd': {'bind': '/etc/passwd', 'mode': 'ro'},
            '/etc/sudoers.d': {'bind': '/etc/sudoers.d', 'mode': 'ro'},
            '/tmp/.X11-unix': {'bind': '/tmp/.X11-unix', 'mode': 'rw'},
            home + '/.Xauthority': {'bind': home + '/.Xauthority', 'mode': 'ro'}
        }
    )
    return nclient
# Only for testing


if __name__ == "__main__":
    run_nclient()
