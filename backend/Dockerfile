# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat && apt-get install -y dos2unix

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install  --no-cache-dir -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app
RUN dos2unix /usr/src/app/entrypoint.sh
#RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
#COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
