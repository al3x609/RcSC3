FROM centos:latest

LABEL name="Proyect SC3" \
	vendor="UIS <Universidad Industiral de Santander>" \
	Description="Imagen base +  openbox + novnc + websockify "\
	license="Private" \
	version="1.0" \
	MAINTAINER="Cesar Bernal <csrbernal609@gmail.com>" \
	build-date="20180322"

ENV REPO_NoVNC 'https://github.com/kanaka/noVNC.git'
ENV REPO_WEBSOCKIFY 'https://github.com/kanaka/websockify'

WORKDIR /opt

RUN yum -y update; yum clean all && \
	yum install -y       \
		numpy            \
		wget             \
		git              \
		unzip            \
		which            \
		net-tools    &&  \
#configuracion novnc    
	git clone $REPO_NoVNC && \
	cd noVNC/utils && \
	git clone $REPO_WEBSOCKIFY websockify && \
	ln -s vnc.html index.html && \
# Clean Seccion
	rm -r /usr/share/info/*            && \
	rm -r /usr/share/man/*             && \
	rm -r /usr/share/doc/*             && \
	find /. -name "*~" -type f -delete && \
	yum clean all                      && \
	rm -rf /var/cache/yum

ENV PATH "/:${PATH}"

ENTRYPOINT ["/usr/bin/sh", "-C", "/opt/noVNC/utils/launch.sh", "--listen", "6080"]
CMD ["--vnc","192.168.66.25:5901"]
