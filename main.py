#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import docker
import subprocess
from novnc import run_nvnc as nv
from paraview import run_pv as pv
from getpass import getuser



class RcSC3(object):

    __display = None
    __listen = None

    def __init__(self, username, user, group, home):
        self.user = user
        self.home = home
        self.group = group
        self.username = username

    def __set_display(self, display_port):
        self.__display = display_port

    def get_display(self):
        return self.__display

    def __set_listen(self, listen_port):
        self.__listen = listen_port

    def get_listen(self):
        return self.__listen

    def start_vnc(self):
        port = 1
        for i in range(1, 10):
            cmd = "/tmp/.X" + str(port) + "-lock"
            if(os.path.isfile(cmd)):
                port += 1
            else:
                name = "' <<ParaView 5.5>> '"
                # cambio de linea incluido PEP8
                cmd = "/opt/TurboVNC/bin/vncserver :" + \
                    str(port) + " -name " + name + " -noxstartup -fg -nohttpd -interframe -mt -nthreads 4"
                subprocess.call(cmd, shell=True)
                break
        self.__set_display(port + 5900)

    def listen_port(self):
        # verifica que el puerto este libre 0: <ocupado> 1: <libre>
        port = 6080
        cmd = "netstat -ltn | grep -qs ':" + str(port) + " .*LISTEN' &&  echo '' "
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        output, ret = p.communicate()[0], p.returncode

        while (ret != 1):
            port += 1
            cmd = "netstat -ltn | grep -qs ':" + str(port) + " .*LISTEN' &&  echo '' "
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            output, ret = p.communicate()[0], p.returncode

        self.__set_listen(port)

    def __clear(self):
        cmd = "/opt/TurboVNC/bin/vncserver -kill :" + str(self.display)
        subprocess.call(cmd, shell=True)

    def menu(self):

        str_tmp = "192.168.66.25:" + str(self.get_display())
        cmd_vnc = ["--vnc", str_tmp]

        client_nvnc = nv.run_nclient(
            listen_port=self.get_listen(),
            cmd=cmd_vnc,
            username=self.username,
            user=self.user,
            group=self.group,
            home=self.home

        )
        client_paraview = pv.run_pclient(
            displayVar=str(self.get_display() - 5900),
            username=self.username,
            user=self.user,
            group=self.group,
            home=self.home
        )

        print ("")
        print ("******************************************************************")
        print ("Bienvenido {}".format(self.username))
        print ("DISPLAY asignada: {}".format(self.get_display()))
        print ("puerto para el tunel {}".format(self.get_listen()))
        print ("en una terminal ingrese el siguiente comando: ")
        print ("ssh -qlNT {} -L 15000:ngrid:{} toctoc.sc3.uis.edu.co".format(self.username, self.get_listen()))
        print ("ingrese a la siguiente URL en su buscador http://127.0.0.1:15000")
        print ("------------------------------------------------------------------")


if __name__ == "__main__":

    c = RcSC3(username=getuser(), user=os.getuid(), group=os.getgid(), home=os.getenv('HOME'))
    print(" user:{} Iduser:{} GdUser:{} home:{}".format(c.username, c.user, c.group, c.home))
#    try:
    subprocess.call("xhost + > /dev/null 2>&1", shell=True)

    c.start_vnc()
    print(" vnc iniciado en disiplay :{}".format(c.get_display()))

    c.listen_port()
    print(" proxy escucha en :{}".format(c.get_listen()))

    c.menu()

    subprocess.call("xhost - > /dev/null 2>&1", shell=True)
#   except Exception:
#    print (" Find a bug in somewhere! :| ")
    # c.clear(display)
