FROM registry.access.redhat.com/rhel7.4

ARG http_proxy=http://genproxy.amdocs.com:8080/
ARG HTTP_PROXY=http://genproxy.corp.amdocs.com:8080/
ARG https_proxy=http://genproxy.amdocs.com:8080/
ARG HTTPS_PROXY=http://genproxy.corp.amdocs.com:8080/
ARG FTP_PROXY=http://genproxy.corp.amdocs.com:8080/
ARG ftp_proxy=http://genproxy.corp.amdocs.com:8080/
ARG no_proxy=localhost,127.0.0.1,.amdocs.com
ARG no_proxy=localhost,127.0.0.1,localaddress,.localdomain.com,illinlic01,linvc04,docker01,/var/run/docker.sock,.sock,.corp.amdocs.com,.amdocs.com,.cloudnative,.cloudnative.corp.amdocs.com
ARG NO_PROXY=localhost,127.0.0.1,localaddress,.localdomain.com,illinlic01,linvc04,docker01,/var/run/docker.sock,.sock,.corp.amdocs.com,.amdocs.com,.cloudnative,.cloudnative.corp.amdocs.com
ARG no_http_proxy=localhost,127.0.0.1,localaddress,.localdomain.com,illinlic01,linvc04,docker01,/var/run/docker.sock,.sock,.corp.amdocs.com,.amdocs.com,.cloudnative,.cloudnative.corp.amdocs.com

COPY amd-external-pci-pmx-10.2.repo /etc/yum.repos.d/amd-external-pci-pmx-10.2.repo
RUN yum install -y oracle-instantclient12.2-sqlplus && \
yum install -y python-pip && \
pip install --upgrade pip && \
yum install -y https://centos7.iuscommunity.org/ius-release.rpm && \
yum install -y python36u python36u-pip && \
rm -f /etc/yum.repos.d/amd-external-pci-pmx-10.2.repo && \
rm -f /etc/yum.repos.d/*.repo && \
yum clean all && \
rm -rf /var/cache/yum && \
ln -sf  /usr/bin/python3.6 /usr/bin/python3  

WORKDIR /root/
COPY index.py           . 
COPY requirements.txt   . 
RUN pip3.6 install -r requirements.txt
COPY function           function 
COPY lib  lib

RUN touch ./function/__init__.py
ENV PAYTHONPATH=${PAYTHONPATH}:lib
WORKDIR /root/function/
COPY function/requirements.txt  .
RUN pip3.6 install -r requirements.txt

ENV ORACLE_HOME /usr/lib/oracle/12.2/client64
ENV PATH ${PATH}:${ORACLE_HOME}/bin
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:/usr/lib/oracle/12.2/client64/lib



# Alternatively use ADD https:// (which will not be cached by Docker builder)
ADD https://github.com/openfaas/faas/releases/download/0.8.0/fwatchdog  /usr/bin/fwatchdog 
RUN chmod +x /usr/bin/fwatchdog

WORKDIR /root/

COPY ./app_login_details.json /usr/local/
COPY ./database_login_details.json /usr/local/
COPY ./servers_login_details.json /usr/local/

ENV fprocess="python3 index.py"

HEALTHCHECK --interval=1s CMD [ -e /tmp/.lock ] || exit 1

CMD ["/usr/bin/fwatchdog"]
