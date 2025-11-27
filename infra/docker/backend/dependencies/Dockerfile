FROM python:3.14.0-alpine
RUN set -ex && apk update
ENV PATH="/root/.cargo/bin/:$PATH"
COPY --from=ghcr.io/astral-sh/uv:0.9.10 /uv /uvx /bin/
WORKDIR /app
COPY ../../backend/ /app 
RUN uv sync --locked
RUN uv add \
    gunicorn \
    opentelemetry-instrumentation \
    opentelemetry-distro \
    opentelemetry-exporter-otlp \
    opentelemetry-instrumentation-django \
    opentelemetry-instrumentation-requests