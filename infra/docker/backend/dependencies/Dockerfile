FROM python:3.14.0-alpine
RUN set -ex \
    && apk update \
    && pip3 install --upgrade pip
WORKDIR /app
COPY ../../backend/swippter/requirements.txt /app/swippter/
WORKDIR /app/swippter
RUN pip3 install --no-cache-dir -r requirements.txt
