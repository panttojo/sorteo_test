FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y wget libssl-dev mariadb-client &&\
    wget -P / https://github.com/ufoscout/docker-compose-wait/releases/download/2.5.1/wait && chmod +x /wait

RUN mkdir -p /usr/src/app && mkdir /var/log/talana && chmod 777 /var/log/talana

WORKDIR /usr/src/app

COPY requirements requirements/
COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements/development.txt

RUN adduser celery-user --disabled-password --gecos ''

EXPOSE 8000
