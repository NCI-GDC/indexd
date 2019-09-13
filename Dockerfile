###########
# BUILDER #
###########

FROM quay.io/ncigdc/apache-base:python3 as build


COPY . /indexd
WORKDIR /indexd

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libssl-dev \
       libffi-dev \
       python3-dev \
    && mkdir -p /src \
    && pip3 install -r requirements.txt \
    && python3 setup.py install


##########
# DEPLOY #
##########

FROM quay.io/ncigdc/apache-base:python3

LABEL org.label-schema.name="indexd" \
      org.label-schema.description="indexd container image" \
      org.label-schema.version="1.0.0" \
      org.label-schema.schema-version="1.0"

RUN mkdir -p /var/www/indexd \
    && a2dissite 000-default \
    && apt-get install -y python3

COPY wsgi.py /var/www/indexd/ 
COPY bin/indexd /var/www/indexd/ 
COPY --from=build /usr/local/lib/python3.5/dist-packages /usr/local/lib/python3.5/dist-packages
COPY --from=build /src /src
COPY . /indexd

WORKDIR /var/www/indexd
