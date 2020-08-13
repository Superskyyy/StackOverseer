
# Dockerfile

# Pull base Python image
FROM python:3.7

# Set environment variables
# Send output to terminal
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Set work directory

RUN mkdir /stack_overseer
WORKDIR /stack_overseer

# Install dependencies
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin
RUN pip install pipenv
COPY Pipfile Pipfile.lock /stack_overseer/
RUN pipenv install --system

COPY . /stack_overseer/