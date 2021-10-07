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
    git clone https://github.com/apache/arrow.git && \
    sed -i '/#define DMLC_LOG_STACK_TRACE 1/d' /build/xgboost/dmlc-core/include/dmlc/base.h && \
    sed -i '/#define DMLC_LOG_STACK_TRACE 1/d' /build/xgboost/rabit/include/dmlc/base.h && \
    sed -i -e '/_EXECINFO_H/,/endif/d' -e '/execinfo/d' /build/arrow/cpp/src/arrow/util/logging.cc &&\
    apk del .build-dependencies

RUN apk add --update --no-cache \
    --virtual=.build-dependencies \
    make cmake gfortran \
    python3-dev \
    py-setuptools g++ && \
    apk add --no-cache openblas lapack-dev libexecinfo-dev libstdc++ libgomp && \
    ln -s locale.h /usr/include/xlocale.h && \
    cd /build/xgboost; make -j4 && \
    cd /build/xgboost/python-package && \
    python3 setup.py install && \
    rm /usr/include/xlocale.h && \
    mkdir /build/arrow/cpp/build && \
    cd /build/arrow/cpp/build && \
    cmake -DCMAKE=release \
          -DCMAKE_INSTALL_LIBDIR=lib \
          -DCMAKE_INSTALL_PREFIX=/usr/local \
          -DARROW_PARQUET=on \
          -DARROW_PYTHON=on \
          -DARROW_PLASMA=on \
          -DARROW_BUILD_TESTS=off \
          .. && \
    make -j$(nproc) && \
    make install && \
    cd /build/arrow/python && \
    python3 setup.py build_ext --build-type=release \
                               --with-parquet \
                               --inplace && \
    py.test pyarrow && \
    rm -rf /build && \
    apk del .build-dependencies
    
RUN apk add --no-cache py3-pip &&\
    apk add --no-cache py3-wheel &&\
    apk add --no-cache py3-setuptools

WORKDIR /app

RUN mkdir /app/commons

COPY prediction /app
COPY commons /app/commons

RUN pip install --no-cache-dir -r requirements-docker.txt
RUN pip install threadpoolctl

CMD ["python3", "-u", "main.py"]
