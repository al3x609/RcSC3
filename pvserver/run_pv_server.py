#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import docker


def run_ps_client(displayVar, user, group, home, username, server_port, np, n_gpu):
    imageName = "al3x609/pserver:5.5"
    containerName = "pserv-" + username
    s_port = "--server-port=" + str(server_port)
    ps_client = docker.from_env()

    if(n_gpu == 1):
        cmd = [
            "-np",
            str(np),
            "pvserver",
            s_port,
            "-display",
            ":0.0",
            "--force-offscreen-rendering"
        ]
    else:
        cmd = [
            "-np",
            str(np),
            "pvserver",
            s_port,
            "-display",
            ":0.0",
            "--force-offscreen-rendering",
            ":",
            "-np",
            str(np),
            "pvserver",
            s_port,
            "-display",
            ":0.1",
            "--force-offscreen-rendering"
        ]

    try:
        ps_client.containers.run(
            user=str(user) + ":" + str(group),
            command=cmd,
            ports={'11111/tcp': server_port},
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
                '/tmp/.X11-unix': {'bind': '/tmp/.X11-unix', 'mode': 'rw'}
            }
        )
    except Exception as e:
        raise e

    return ps_client


if __name__ == "__main__":
    run_ps_client()
