# This instruction sets the Python image at runtime
FROM python:3.8.11-slim-buster

# It ensures that the Python output is set straight to
# the terminal without buffering it first
ENV PYTHONUNBUFFERED 1

# necessary to work the file ./wait-for to use at command for api container.
RUN apt-get -y update && apt-get install -y \
    build-essential \
    cmake \
    pkg-config \
    gcc \
    git \
    libcurl4-openssl-dev \
    libssl-dev \
    netcat

# Creates ssh directory to save the ssh keys
RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan gitlab.com >> ~/.ssh/known_hosts

# Install dlib as required by the face_recognition
RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS

# Upgrade pip if necessary
RUN pip install --upgrade pip

# Install packages that help in development
COPY ./requirements/dev.txt /tmp/dev.txt
RUN pip install -r /tmp/dev.txt

# Install any needed packages to run the tests
COPY ./requirements/test.txt /tmp/test.txt
RUN pip install -r /tmp/test.txt

# Install any needed packages specified in base
COPY ./requirements/base.txt /tmp/base.txt
RUN pip install -r /tmp/base.txt

# Sets the working directory for our project in the container
WORKDIR /var/task/

# Adds our working directory to the Python path
ENV PYTHONPATH "${PYTHONPATH}:/var/task:/var/task/facebook"
