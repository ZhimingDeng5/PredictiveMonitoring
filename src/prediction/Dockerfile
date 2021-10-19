FROM centos:8

# RUN yum -y updata
# RUN yum -y install gcc gcc-c++
# RUN yum -y install gcc automake autoconf libtool make
# RUN yum -y groupinstall 'Development Tools'
# RUN yum -y install gcc openssl-devel bzip2-devel libffi-devel
# RUN dnf -y install python3
RUN yum -y update
RUN yum -y groupinstall "Development Tools"
RUN yum -y install openssl-devel bzip2-devel libffi-devel xz-devel
RUN yum -y install wget
RUN wget https://www.python.org/ftp/python/3.8.9/Python-3.8.9.tgz
RUN tar xvf Python-3.8.9.tgz && cd Python-3.8.9/ &&  ./configure --enable-optimizations && make altinstall

WORKDIR /app

RUN mkdir /app/commons

COPY prediction /app
COPY commons /app/commons

RUN pip3.8 install -r requirements.txt
RUN pip3.8 install threadpoolctl

CMD ["python3.8", "-u", "main.py"]
