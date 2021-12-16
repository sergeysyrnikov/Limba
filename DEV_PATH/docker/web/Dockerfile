FROM python:3.8

COPY ./limba /srv/www/limba
WORKDIR /srv/www/limba

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN apk update \
#     && apk add jpeg-dev zlib-dev libjpeg \
#     && apk add --update --no-cache curl jq py3-configobj py3-pip py3-setuptools python3 python3-dev \
#     && apk add postgresql-dev gcc python3-dev musl-dev && apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python \
#     apk add wkhtmltopdf xvfb


RUN pip install -r requirements.txt