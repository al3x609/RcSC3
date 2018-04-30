#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import docker
import subprocess
import run_nvnc as nv
import run_pv as pv
import run_pv_server as spv
from getpass import getuser
from optparse import OptionParser


class RcSC3(object):

    __display = None
    __listen_proxy = None
    __pv_server_port = None

    def __init__(self, username, user, group, home):
        self.user = user
        self.home = home
        self.group = group
        self.username = username

    def __set_display(self, display_port):
        self.__display = display_port

    def get_display(self):
        return self.__display

    def __set_server_port(self, server_port):
        self.__pv_server_port = server_port

    def get_server_port(self):
        return self.__pv_server_port

    def __set_listen_proxy(self, listen_port):
        self.__listen_proxy = listen_port

    def get_listen_proxy(self):
        return self.__listen_proxy

    def start_vnc(self):
        port = 1
        cmd = "/tmp/.X" + str(port) + "-lock"
        while (os.path.isfile(cmd)):
            port += 1
            cmd = "/tmp/.X" + str(port) + "-lock"
        if(port < 10):
            name = "' <<ParaView 5.5>> '"
            # cambio de linea incluido PEP8
            cmd = "/opt/TurboVNC/bin/vncserver :" + \
                str(port) + " -name " + name + " -noxstartup -fg -nohttpd -interframe -mt -nthreads 4"
            subprocess.call(cmd, shell=True)
            self.__set_display(display_port=port + 5900)
            return True
        else:
            return False

    def free_port(self, port_base):
        # verifica que el puerto este libre 0: <ocupado> 1: <libre>
        port = port_base
        cmd = "netstat -ltn | grep -qs ':" + str(port) + " .*LISTEN' &&  echo '' "
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        output, ret = p.communicate()[0], p.returncode

        while (ret != 1):
            port += 1
            cmd = "netstat -ltn | grep -qs ':" + str(port) + " .*LISTEN' &&  echo '' "
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            output, ret = p.communicate()[0], p.returncode

        return port
        # self.__set_listen(port)  # return port for proxy novnc

    def port_server_paraview(self):
        self.__set_server_port(server_port=self.free_port(port_base=11111))

    def port_proxy_nvnc(self):
        self.__set_listen_proxy(listen_port=self.free_port(port_base=6080))

    def __clear(self):
        cmd = "/opt/TurboVNC/bin/vncserver -kill :" + str(self.get_display())
        subprocess.call(cmd, shell=True)

    def services(self, parallel, np_mpi, n_gpu):
        self.port_server_paraview()

        if(parallel):
            server_paraview = spv.run_ps_client(
                displayVar=str(self.get_display() - 5900),
                user=self.user,
                group=self.group,
                home=self.home,
                username=self.username,
                server_port=self.get_server_port(),
                np=np_mpi,
                n_gpu=n_gpu
            )

        client_paraview = pv.run_pclient(
            displayVar=str(self.get_display() - 5900),
            username=self.username,
            user=self.user,
            group=self.group,
            home=self.home,
            server_port=self.get_server_port(),
            paralelo=parallel
        )

        str_tmp = "192.168.66.25:" + str(self.get_display())
        cmd_vnc = ["--vnc", str_tmp]
        self.port_proxy_nvnc()
        client_nvnc = nv.run_nclient(
            listen_port=self.get_listen_proxy(),
            cmd=cmd_vnc,
            username=self.username,
            user=self.user,
            group=self.group,
            home=self.home
        )

    def menu(self):

        print ("")
        print ("******************************************************************")
        print ("Bienvenido {}".format(self.username))
        print ("DISPLAY asignada: {}".format(self.get_display()))
        print ("puerto para el tunel {}".format(self.get_listen_proxy()))
        print ("en una terminal ingrese el siguiente comando: ")
        print ("ssh -qlNT {} -L 15000:ngrid:{} toctoc.sc3.uis.edu.co".format(self.username, self.get_listen_proxy()))
        print ("ingrese a la siguiente URL en su buscador http://127.0.0.1:15000")
        print ("------------------------------------------------------------------")


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option('-p', '--parallel', dest='parallel', action='store_true',
                      default=False,
                      help='select parallel mode paraview (default False)')
    parser.add_option('-n', '--nprocess', dest='np', action='store',
                      type="int", default=1,
                      help='set proccess number mpi (default 1)')
    parser.add_option('-g', '--n_gpu', dest='ngpu', action='store',
                      type="int", default=1,
                      help='set the gpu num to connect to (default 1 of 2)')
    (options, args) = parser.parse_args()

    c = RcSC3(username=getuser(), user=os.getuid(), group=os.getgid(), home=os.getenv('HOME'))

    subprocess.call("xhost + > /dev/null 2>&1", shell=True)

    if(c.start_vnc()):

        c.port_proxy_nvnc()  # set port novnc proxy
        c.services(parallel=options.parallel, np_mpi=options.np,
                   n_gpu=options.ngpu)  # start services by args main
        c.menu()  # show info to conexion
    else:
        print(" We no have any free service")

    subprocess.call("xhost - > /dev/null 2>&1", shell=True)
