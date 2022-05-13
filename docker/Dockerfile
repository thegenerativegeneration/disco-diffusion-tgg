# https://docs.nvidia.com/deeplearning/frameworks/pytorch-release-notes/rel_22-03.html#rel_22-03

FROM nvcr.io/nvidia/pytorch:22.03-py3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install a few dependencies
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install -y tzdata imagemagick

# Create a disco user
RUN useradd -ms /bin/bash disco
USER disco

# Set up code directories
RUN mkdir -p models

ARG REPO=https://github.com/entmike/disco-diffusion-1.git

COPY docker-requirements.txt docker-requirements.txt
RUN pip install -r docker-requirements.txt

# Clone Git repositories
RUN git clone $REPO 