FROM centos:latest

LABEL name="Proyect SC3" \
    Description="Imagen base +  VirtualGL + ParaView-5 "\
    MAINTAINER="Cesar Bernal <csrbernal609@gmail.com>" \
    vendor="UIS <Universidad Industiral de Santander>" \
    build-date="20180322" \
    license="Private" \
    version="1.0" 

ENV NVIDA_RUN 'http://us.download.nvidia.com/XFree86/Linux-x86_64/367.124/NVIDIA-Linux-x86_64-367.124.run'
ENV VIRTUALGL_RUN 'https://sourceforge.net/projects/virtualgl/files/2.5.2/VirtualGL-2.5.2.x86_64.rpm'

WORKDIR /opt

RUN yum -y update; yum clean all && \
    yum install -y       \
        wget             \
        libXt            \
        libSM            \
        deltarpm         \
        qt5-qtbase-gui   && \
#configuration openbox
    wget  'https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm'  && \
    yum install -y \
        epel-release-latest-7.noarch.rpm \
        openbox && \
# configuration nvida applications
    wget -L $NVIDA_RUN  && \
    chmod +x NVIDIA-Linux-x86_64-367.124.run && \
    ./NVIDIA-Linux-x86_64-367.124.run --no-kernel-module-source -z --no-kernel-module -N -b -a -s -q --no-x-check && \
    nvidia-xconfig --use-display-device=none --virtual=1920x1200 && \
# configuration VirtualGL
    curl -SL $VIRTUALGL_RUN -o VirtualGL-2.5.2.x86_64.rpm && \
    yum -y --nogpgcheck localinstall VirtualGL-2.5.2.x86_64.rpm  && \
    /opt/VirtualGL/bin/vglserver_config -config +s +f -t && \
# Clean Section
    rm NVIDIA-Linux-x86_64-367.124.run && \
    rm VirtualGL-2.5.2.x86_64.rpm      && \
    rm -r /usr/share/info/*            && \
    rm -r /usr/share/man/*             && \
    rm -r /usr/share/doc/*             && \
    find /. -name "*~" -type f -delete && \
    yum clean all                      && \
    rm -rf /var/cache/yum

ADD ./packages/ParaView.tar.gz /opt
ENV PATH /opt/VirtualGL/bin:/opt/ParaView/bin:${PATH}
ENTRYPOINT ["/opt/VirtualGL/bin/vglrun"]
CMD ["paraview"]
