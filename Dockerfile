FROM node:10-alpine

ENV DJANGO_SETTINGS_MODULE=crudlfap_example.settings
ENV UWSGI_MODULE=crudlfap_example.wsgi:application

ENV NODE_ENV=production
ENV PATH="${PATH}:/app/.local/bin"
ENV PLAYLABS_PLUGINS=postgres,uwsgi,django,sentry
ENV PYTHONIOENCODING=UTF-8 PYTHONUNBUFFERED=1
ENV STATIC_URL=/static/ STATIC_ROOT=/app/static
ENV UWSGI_SPOOLER_NAMES=mail,stat UWSGI_SPOOLER_MOUNT=/app/spooler
ENV VIRTUAL_PROTO=uwsgi
EXPOSE 6789

RUN apk update && apk --no-cache upgrade && apk --no-cache add shadow python3 py3-psycopg2 uwsgi-python3 uwsgi-http uwsgi-spooler dumb-init bash git curl && pip3 install --upgrade pip
RUN mkdir -p /app && usermod -d /app -l app node && groupmod -n app node && chown -R app:app /app
WORKDIR /app

USER app
RUN mkdir -p ${STATIC_ROOT} && mkdir -p ${UWSGI_SPOOLER_MOUNT}

COPY --chown=app:app js /app/js
RUN cd /app/js && yarn install --frozen-lockfile

COPY --chown=app:app setup.py README.rst MANIFEST.in /app/
COPY --chown=app:app src /app/src
RUN cd /app && pip3 install --user --editable /app[dev]

RUN DEBUG=1 django-admin collectstatic --noinput --link

CMD /usr/bin/dumb-init uwsgi \
  --spooler=${UWSGI_SPOOLER_MOUNT}/mail \
  --spooler=${UWSGI_SPOOLER_MOUNT}/stat \
  --spooler-processes 8 \
  --socket=0.0.0.0:6789 \
  --chdir=/app \
  --plugin=python3,http \
  --module=${UWSGI_MODULE} \
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
  --static-map ${STATIC_ROOT}=${STATIC_URL}
