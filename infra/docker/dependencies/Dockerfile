FROM python:3.14.0-alpine
RUN set -ex && apk update && apk add --no-cache build-base gcc mysql-dev mariadb-dev && \
    rm -rf /var/cache/apk/*    
ENV PATH="/root/.cargo/bin/:$PATH"
COPY --from=ghcr.io/astral-sh/uv:0.9.10 /uv /uvx /bin/
WORKDIR /app
COPY ../../backend/ /app 
RUN uv sync --locked
RUN source .venv/bin/activate