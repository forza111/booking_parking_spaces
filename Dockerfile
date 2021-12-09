# pull official base image
FROM python:3.8.3-alpine
# set work directory
WORKDIR /code/
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --system --dev

COPY . /code/
