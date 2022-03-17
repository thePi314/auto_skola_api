FROM python:3.9-buster

ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN apt-get update -y && apt-get install build-essential python-dev -y

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./compose/entrypoint /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/start /start
RUN chmod +x /start

COPY ./compose/start-worker /start-worker
RUN chmod +x /start-worker


ADD . /code/

WORKDIR /code

ENTRYPOINT ["/entrypoint"]
