FROM continuumio/miniconda3:4.7.10
MAINTAINER data-recsys@traveloka.com

# set up environment
RUN apt-get update && apt-get install --no-install-recommends --yes \
    build-essential \
    make \
    && rm -rf /var/lib/apt/lists/*

# install larger packages
RUN conda install --name base --quiet --yes \
    pip=19.2.* \
    python=3.7.4 \
    && pip install --no-cache-dir \
    meinheld==1.0.*

# remove unneeded environment
RUN apt-get remove --purge --autoremove --yes \
    build-essential

COPY environment.yml environment.yml
RUN conda env update --name base --file environment.yml --prune --quiet \
    && conda clean --all --yes \
    && conda list

WORKDIR app

COPY configs configs
COPY Makefile Makefile
COPY src src

CMD ["make", "gunicorn"]
