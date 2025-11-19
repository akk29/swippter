FROM python:3.13.3-alpine
ENV PATH="/root/.cargo/bin/:$PATH"
RUN set -ex \
    && apk update 
COPY --from=ghcr.io/astral-sh/uv:0.9.10 /uv /uvx /bin/
WORKDIR /app
COPY . /app
RUN uv sync --locked
RUN source .venv/bin/activate
EXPOSE 8000
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app/swippter
RUN ["python", "manage.py", "makemigrations", "app"]
RUN ["python", "manage.py", "migrate", "app"]
RUN ["python", "manage.py", "makemigrations"]
RUN ["python", "manage.py", "migrate"]
RUN ["python", "manage.py", "collectstatic", "--noinput"]
CMD ["gunicorn", "swippter.wsgi", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "4"]
