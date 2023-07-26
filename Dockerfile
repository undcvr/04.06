FROM python:3.10-alpine3.18

COPY ./requirements.txt /temp/requirements.txt
COPY ./library-project /library-project
WORKDIR /library-project
EXPOSE 8000

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password project-user 
USER project-user