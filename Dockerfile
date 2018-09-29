FROM node:10-alpine

ENV DJANGO_SETTINGS_MODULE crudlfap_example.settings
ENV NODE_ENV production
ENV PLAYLABS_PLUGINS postgres,uwsgi,django,sentry
ENV PYTHONIOENCODING UTF-8
ENV PYTHONUNBUFFERED 1
ENV STATIC_URL /static/
ENV STATIC_ROOT /app/static
ENV UWSGI_SPOOLER_NAMES mail,stat
ENV UWSGI_SPOOLER_MOUNT /spooler
ENV VIRTUAL_PROTO uwsgi
EXPOSE 6789

RUN mkdir -p ${STATIC_ROOT}

RUN apk update && apk --no-cache upgrade && apk --no-cache add shadow python3 py3-psycopg2 uwsgi-python3 uwsgi-http uwsgi-spooler dumb-init bash git curl
RUN adduser -h /app -D app
WORKDIR /app

ADD js /app/js
RUN cd /app/js && yarn install --frozen-lockfile

RUN pip3 install --upgrade pip
COPY setup.py README.rst MANIFEST.in /app/
ADD src /app/src
RUN cd /app && pip3 install --editable /app[dev]

RUN crudlfap collectstatic --noinput
USER app

CMD /usr/bin/dumb-init uwsgi \
  --spooler=/spooler/mail \
  --spooler=/spooler/stat \
  --spooler-processes 8 \
  --socket=0.0.0.0:6789 \
  --chdir=/app \
  --plugin=python3,http \
  --module=$DJANGO_SETTINGS_MODULE \
  --http-keepalive \
  --harakiri=120 \
  --max-requests=100 \
  --master \
  --workers=24 \
  --processes=12 \
  --chmod=666 \
  --log-5xx \
  --vacuum \
  --enable-threads \
  --reload-os-env \
  --post-buffering=8192 \
  --ignore-sigpipe \
  --ignore-write-errors \
  --disable-write-exception \
  --static-map $STATIC_ROOT=$STATIC_URL
