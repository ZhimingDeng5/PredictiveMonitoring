FROM centos:8

# RUN yum -y upgrade
# RUN yum -y install gcc gcc-c++
# RUN yum -y install gcc automake autoconf libtool make
# RUN yum -y groupinstall 'Development Tools'
# RUN yum -y install gcc openssl-devel bzip2-devel libffi-devel
RUN dnf -y install python3

WORKDIR /app

RUN mkdir /app/commons

COPY prediction /app
COPY commons /app/commons

RUN pip3 install -r requirements-docker.txt
RUN pip3 install threadpoolctl

CMD ["python3", "-u", "main.py"]
