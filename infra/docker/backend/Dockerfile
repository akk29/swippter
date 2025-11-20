FROM backend-dependencies:latest
COPY ../../backend/ /app
WORKDIR /app/swippter
RUN ["python", "manage.py", "makemigrations", "app"]
RUN ["python", "manage.py", "migrate", "app"]
RUN ["python", "manage.py", "makemigrations"]
RUN ["python", "manage.py", "migrate"]
RUN ["python", "manage.py", "collectstatic", "--no-input"]
CMD ["gunicorn", "swippter.wsgi", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "4"]
