FROM python:3.14.0-alpine
RUN set -ex && apk update && apk add --no-cache build-base gcc mysql-dev mariadb-dev && \
    rm -rf /var/cache/apk/*    
ENV PATH="/root/.cargo/bin/:$PATH"
COPY --from=ghcr.io/astral-sh/uv:0.9.10 /uv /uvx /bin/
RUN adduser -D appuser \
 && mkdir -p /app \
 && chown -R appuser:appuser /app
WORKDIR /app
COPY ../../backend/ /app 
RUN uv sync --locked
RUN uv add \
    opentelemetry-distro \
    opentelemetry-exporter-otlp \
    opentelemetry-instrumentation-django \
    opentelemetry-instrumentation-wsgi \
    opentelemetry-instrumentation-requests \
    opentelemetry-instrumentation-gunicorn
RUN source .venv/bin/activate
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app/swippter
EXPOSE 8000
COPY infra/docker/server/entrypoint.sh /app/swippter/entrypoint.sh
RUN chmod +x /app/swippter/entrypoint.sh
ENTRYPOINT ["/app/swippter/entrypoint.sh"]