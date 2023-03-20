# Dockerfile to run the CI checks and verify that the project can indeed be
# bootstrapped properly.

FROM python:3.9-bullseye
ENV PYTHONUNBUFFERED 1
ARG USERID=1000

RUN apt-get update && apt-get install -y --no-install-recommends \
        pkg-config \
        build-essential \
        git \
        libpq-dev \
        python3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install virtualenv

WORKDIR /ci

COPY ./run_ci.sh /ci/run_ci.sh

RUN useradd -m -u $USERID maykin \
    && chown -R maykin:maykin /ci

# drop privileges
USER maykin

ENV DB_HOST=/var/run/postgresql

# !! Ensure that:
#
# * the postgresql run directory (/var/run/postgresql/) is mounted
CMD ["/ci/run_ci.sh"]
