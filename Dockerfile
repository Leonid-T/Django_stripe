FROM python:3.11-slim

WORKDIR /usr/src/app

RUN apt-get update && apt install -y netcat

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./srv ./srv

WORKDIR ./srv
ENTRYPOINT ["/usr/src/app/srv/entrypoint.sh"]

CMD gunicorn srv.wsgi:application