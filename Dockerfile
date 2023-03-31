FROM python:3.10-slim as builder
LABEL maintainer="André Felipe Dias <andref.dias@gmail.com>"

USER root

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y --no-install-recommends build-essential libffi-dev libxml2-dev \
    libxslt-dev curl libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ENV POETRY_VERSION=1.4.1
RUN curl https://install.python-poetry.org | python -

RUN python -m venv /venv
ENV PATH=/venv/bin:/root/.local/bin:${PATH}

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN . /venv/bin/activate; \
    poetry install --no-dev

# ---------------------------------------------------------

FROM python:3.10-slim as final


RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /venv /venv
ENV PATH=/venv/bin:${PATH}

WORKDIR /app
USER nobody
COPY --chown=nobody:nogroup entrypoint.sh migrate_database.py hypercorn.toml alembic.ini ./
COPY --chown=nobody:nogroup alembic/ ./alembic
COPY --chown=nobody:nogroup url_shortener/ ./url_shortener

EXPOSE 5000

CMD ["./entrypoint.sh"]
