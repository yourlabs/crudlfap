FROM ubuntu:artful

# utf8
ENV PYTHONIOENCODING UTF-8
ENV PYTHONUNBUFFERED 1

RUN apt update -y && apt upgrade -y && apt install -y bash dumb-init python3 python3-pip gettext curl
RUN curl -sL https://deb.nodesource.com/setup_9.x | bash -
RUN apt install -y nodejs
RUN npm install -g yarn

RUN useradd -md /code code
WORKDIR /code
EXPOSE 8000

COPY webpack.config.js yarn.lock .babelrc package.json /code/
ADD js /code/js
RUN yarn install --frozen-lockfile

RUN pip3 install --upgrade pip
COPY setup.py README.rst /code/
ADD src /code/src
RUN pip3 install --editable /code[dev]

ARG GIT_COMMIT
ENV GIT_COMMIT ${GIT_COMMIT}

CMD su code -c '/usr/bin/dumb-init crudlfap dev 0:8000'
