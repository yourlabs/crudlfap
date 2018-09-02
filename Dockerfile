FROM node:9-alpine

# utf8
ENV PYTHONIOENCODING UTF-8
ENV PYTHONUNBUFFERED 1

RUN apk update -y && apk add python3 dumb-init gettext

RUN adduser -h /code -D code
WORKDIR /code
EXPOSE 8000

ADD js /code/js
RUN cd /code/js && yarn install --frozen-lockfile

RUN pip3 install --upgrade pip
COPY setup.py README.rst /code/
ADD src /code/src
RUN cd /code && pip3 install --editable /code[dev]

ARG GIT_COMMIT
ENV GIT_COMMIT ${GIT_COMMIT}

USER code
CMD /usr/bin/dumb-init crudlfap dev 0:8000
