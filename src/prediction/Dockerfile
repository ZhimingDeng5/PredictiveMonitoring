FROM alpine:edge

RUN apk add --update --no-cache

RUN apk add --no-cache py3-pandas=1.3.2-r0 &&\
    apk add --no-cache py3-numpy=1.21.1-r0 &&\
    apk add --no-cache py3-scikit-learn=0.24.0-r1 &&\
    apk add --no-cache py3-scipy=1.7.1-r0 &&\
    apk add --no-cache py3-six=1.15.0-r1 &&\
    apk add --no-cache py3-arrow=0.17.0-r1 &&\
    apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing py3-confluent-kafka=1.7.0-r0

RUN apk add --virtual=.build-dependencies \
    git && \
    mkdir /build && \
    cd /build && \
    git clone --recursive -b v0.81 https://github.com/dmlc/xgboost && \
    sed -i '/#define DMLC_LOG_STACK_TRACE 1/d' /build/xgboost/dmlc-core/include/dmlc/base.h && \
    sed -i '/#define DMLC_LOG_STACK_TRACE 1/d' /build/xgboost/rabit/include/dmlc/base.h && \
    apk del .build-dependencies

RUN apk add --update --no-cache \
    --virtual=.build-dependencies \
    make gfortran \
    python3-dev \
    py-setuptools g++ && \
    apk add --no-cache openblas lapack-dev libexecinfo-dev libstdc++ libgomp && \
    ln -s locale.h /usr/include/xlocale.h && \
    cd /build/xgboost; make -j4 && \
    cd /build/xgboost/python-package && \
    python3 setup.py install && \
    rm /usr/include/xlocale.h && \
    rm -rf /build && \
    apk del .build-dependencies

RUN apk add --no-cache py3-pip &&\
    apk add --no-cache py3-wheel &&\
    apk add --no-cache py3-setuptools

WORKDIR /app

COPY . /app
COPY ../commons /app/commons

RUN pip install --no-cache-dir -r requirements-docker.txt
RUN pip install threadpoolctl

CMD ["python3", "-u", "main.py"]
