#!/usr/bin/env python
# -*- coding: utf-8 -*-

import docker
import os

route = os.path.dirname(os.path.abspath(__file__))

client = docker.from_env()

client.images.build(
    path=route,
    tag="al3x609/nvnc:latest",
    rm=True
)
