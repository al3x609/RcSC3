#!/usr/bin/env python
# -*- coding: utf-8 -*-

import docker
import os

route = os.path.dirname(os.path.abspath(__file__))

client = docker.DockerClient(base_url='tcp://192.168.66.25:2376')

client.images.build(
    path=route,
    tag="al3x609/paraview:5.5",
    rm=True
)
