FROM python:3.10-slim-buster

RUN apt-get -y update && \
	apt-get -y upgrade && \
	apt install -y pigz

ADD . /app
WORKDIR /app

RUN mkdir -p results
RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "/app/main.py", "/app/assets"]
