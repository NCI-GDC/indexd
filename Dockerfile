FROM quay.io/ncigdc/apache-base:2.4.18-1.0.0 as build


COPY . /indexd
WORKDIR /indexd

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    python2.7 \
    python-dev \
    python-pip \
    python-setuptools \
    libpq-dev \
    gcc \
 && pip install wheel \
 && pip install -r build/requirements.txt 

FROM quay.io/ncigdc/apache-base:2.4.18-1.0.0

LABEL org.label-schema.name="indexd" \
      org.label-schema.description="indexd container image" \
      org.label-schema.version="1.0.0" \
      org.label-schema.schema-version="1.0"

RUN mkdir -p /var/www/indexd/ \
    && chmod 777 /var/www/indexd 

COPY wsgi.py /var/www/indexd/ 
COPY bin/indexd /var/www/indexd/ 
COPY --from=build /usr/local/lib/python2.7/dist-packages /usr/local/lib/python2.7/dist-packages

WORKDIR /var/www/indexd


