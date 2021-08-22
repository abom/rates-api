# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install netcat -y
ADD https://raw.githubusercontent.com/eficode/wait-for/v2.1.3/wait-for /wait-for
RUN chmod +x /wait-for
COPY . /code/
