FROM centos:8

RUN dnf -y install python3

WORKDIR /app

RUN mkdir /app/commons

COPY training /app
COPY commons /app/commons

RUN pip3 install -r requirements-docker.txt
RUN pip3 install threadpoolctl

CMD ["python3", "-u", "main.py"]
