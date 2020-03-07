FROM python:3.7.1-slim-stretch

ARG redis_host=""
ARG redis_port="6379"

ADD . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV redis_host $redis_host
ENV redis_port $redis_port

CMD ["python","counter-service.py"]
