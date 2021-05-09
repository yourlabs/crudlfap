FROM archlinux

ENV DJANGO_SETTINGS_MODULE=crudlfap_example.settings
ENV UWSGI_MODULE=crudlfap_example.wsgi:application

ENV NODE_ENV=production
ENV PATH="${PATH}:/app/.local/bin"
ENV PYTHONIOENCODING=UTF-8 PYTHONUNBUFFERED=1
ENV STATIC_URL=/static/ STATIC_ROOT=/app/public
EXPOSE 8000

RUN pacman -Syu --noconfirm mailcap which gettext python python-pillow python-psycopg2 python-pip python-psutil git curl uwsgi uwsgi-plugin-python python python-hiredis libsass && pip install --upgrade pip djcli
RUN useradd --home-dir /app --uid 1000 app && mkdir -p /app && chown -R app /app
WORKDIR /app

COPY setup.py README.rst MANIFEST.in /app/
COPY src /app/src
COPY manage.py /app
RUN pip install --editable /app[project]

RUN ./manage.py ryzom_bundle
RUN DEBUG=1 ./manage.py collectstatic --noinput
RUN find public -type f | xargs gzip -f -k -9

USER app

ARG GIT_COMMIT
ARG GIT_TAG
ENV GIT_COMMIT="${GIT_COMMIT}" GIT_TAG="${GIT_TAG}"

CMD bash -c "djcli dbcheck && ./manage.py migrate --noinput && uwsgi \
  --http-socket=0.0.0.0:8000 \
  --chdir=/app \
  --plugin=python \
  --module=${UWSGI_MODULE} \
  --http-keepalive \
  --harakiri=120 \
  --max-requests=100 \
  --master \
  --workers=8 \
  --processes=4 \
  --chmod=666 \
  --log-5xx \
  --vacuum \
  --enable-threads \
  --post-buffering=8192 \
  --ignore-sigpipe \
  --ignore-write-errors \
  --disable-write-exception \
  --mime-file /etc/mime.types \
  --route '^/static/.* addheader:Cache-Control: public, max-age=7776000' \
  --route '^/js|css|fonts|images|icons|favicon.png/.* addheader:Cache-Control: public, max-age=7776000' \
  --static-map /static=/app/public \
  --static-map /media=/app/media \
  --static-gzip-all"
