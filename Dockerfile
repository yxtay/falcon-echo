FROM python:3.8.0-slim
MAINTAINER wyextay@gmail.com

# set up environment
RUN apt-get update && apt-get install --no-install-recommends --yes \
    build-essential \
    make \
    && rm -rf /var/lib/apt/lists/*

# install larger packages
RUN pip install --no-cache-dir \
    grpcio==1.16.* \
    meinheld==1.0.* \
    pip==19.3.*

# remove unneeded environment
RUN apt-get remove --purge --autoremove --yes \
    build-essential

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt\
    && pip freeze

WORKDIR app

COPY configs configs
COPY Makefile Makefile
COPY src src

ARG ENVIRONMENT=prod
ENV ENVIRONMENT $ENVIRONMENT

CMD ["make", "gunicorn"]
