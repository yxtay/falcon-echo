##
# base
##
FROM python:3.7.4-slim AS base
MAINTAINER wyextay@gmail.com

RUN apt-get update && apt-get install --no-install-recommends --yes \
    make \
    && rm -rf /var/lib/apt/lists/*

# set up user
RUN groupadd -g 999 appuser && \
    useradd -r -u 999 -g appuser --create-home appuser
USER appuser

# set up environment
ENV HOME=/home/appuser
ENV VIRTUAL_ENV=$HOME/venv
ENV PATH=$VIRTUAL_ENV/bin:$PATH
WORKDIR $HOME

# set up python
RUN python -m venv $VIRTUAL_ENV && \
    python -m pip install -U pip

##
# builder
##
FROM base as builder

USER root
RUN apt-get update && apt-get install --no-install-recommends --yes \
    gcc \
    libc-dev \
    && \
    rm -rf /var/lib/apt/lists/*

USER appuser
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt && \
    python -m pip freeze

COPY configs configs
COPY Makefile Makefile
COPY src src

ARG ENVIRONMENT=prod
ENV ENVIRONMENT $ENVIRONMENT
CMD ["make", "gunicorn"]

##
# app
##
FROM base AS app
COPY --from=builder $HOME $HOME

ARG ENVIRONMENT=prod
ENV ENVIRONMENT=$ENVIRONMENT
CMD ["make", "gunicorn"]
