#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import docker

#displayVar = '1'
#user = '0'
#group = '0'
#home = '/root'
#username = 'root'


def run_pclient(displayVar, user, group, home, username):
    imageName = "al3x609/paraview:5.5"
    containerName = "pview-" + username
    pclient = docker.from_env()

    try:
        pclient.containers.run(
            user=str(user) + ":" + str(group),
            detach=True,
            auto_remove=True,
            image=imageName,
            runtime="nvidia",
            working_dir=home,
            name=containerName,
            hostname=containerName,
            environment=[
                "NVIDIA_DRIVER_CAPABILITIES=all",
                "NVIDIA_VISIBLE_DEVICES=all",
                "QT_X11_NO_MITSHM=1",
                "USER=" + username,
                "DISPLAY=:" + displayVar,
                "VGL_LOGO=1",
                "QT_XKB_CONFIG_ROOT=/usr/share/X11/xkb",
                "LIBGL_DEBUG=verbose"
            ],
            volumes={
                home: {'bind': home, 'mode': 'rw'},
                '/etc/group': {'bind': '/etc/group', 'mode': 'ro'},
                '/etc/shadow': {'bind': '/etc/shadow', 'mode': 'ro'},
                '/etc/passwd': {'bind': '/etc/passwd', 'mode': 'ro'},
                '/etc/sudoers.d': {'bind': '/etc/sudoers.d', 'mode': 'ro'},
                '/tmp/.X11-unix': {'bind': '/tmp/.X11-unix', 'mode': 'rw'},                
            }
        )
    except Exception as e:
        raise e

    return pclient


if __name__ == "__main__":
    run_pclient()
