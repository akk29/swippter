FROM backend-dependencies:latest
RUN source .venv/bin/activate
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app/swippter
RUN ["python", "manage.py", "makemigrations", "app"]
RUN ["python", "manage.py", "migrate", "app"]
RUN ["python", "manage.py", "makemigrations"]
RUN ["python", "manage.py", "migrate"]
RUN ["python", "manage.py", "collectstatic", "--no-input"]
EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE=swippter.settings
CMD ["opentelemetry-instrument","gunicorn", "swippter.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "4"]