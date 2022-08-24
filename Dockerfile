FROM python:3.10-slim as builder
LABEL maintainer="André Felipe Dias <andref.dias@gmail.com>"

USER root

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y --no-install-recommends build-essential libffi-dev libxml2-dev \
    libxslt-dev curl libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

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
COPY --chown=nobody:nogroup hypercorn.toml .
COPY --chown=nobody:nogroup url_shortener/ ./url_shortener

EXPOSE 5000

CMD ["hypercorn", "--config=hypercorn.toml", "url_shortener.main:app"]
