#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import docker
# import os
# import getpass
# parser = OptionParser()

# parser.add_option('-d', '--display', dest='display_num', action='store',
#                   type='str', default=' 5901',
#                   help='set display num to connect'
#                   )

# parser.add_option('-l', '--listen', dest='listen_port', action='store',
#                   type='str', default='6080',
#                   help='listen port to proxy noVNC'
#                   )

# (options, args) = parser.parse_args()


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
    )
    return nclient
# Only for testing


if __name__ == "__main__":
    run_nclient()
