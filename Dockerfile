FROM ubuntu:latest

RUN apt update
RUN apt install python3.10 -y
RUN apt install python3-pip -y
RUN apt install wget zip -yum

WORKDIR /app
COPY ./app/requirement.txt /app/requirement.txt

RUN pip install -q -U google-generativeai

RUN pip install -r /app/requirement.txt

EXPOSE 8000
