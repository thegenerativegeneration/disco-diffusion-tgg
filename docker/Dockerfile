FROM pytorch/pytorch

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV DEBIAN_FRONTEND noninteractive\
    SHELL=/bin/bash

# Install a few dependencies
RUN apt-get update --yes && \
    # - apt-get upgrade is run to patch known vulnerabilities in apt-get packages as
    #   the ubuntu base image is rebuilt too seldom sometimes (less than once a month)
    apt-get upgrade --yes && \
    apt install --yes --no-install-recommends\
    wget\
    bash\
    git\
    make\
    gcc-5\
    g++-5\
    build-essential\
    tzdata\
    imagemagick\
    ffmpeg\
    zip\
    unzip\
    openssh-server &&\
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen

# Loosen up /workspace perms
RUN chmod a+rw /workspace

# Create a disco user
RUN useradd -ms /bin/bash disco
USER disco

ARG REPO=https://github.com/entmike/disco-diffusion-1.git
ARG DD_VERSION=2.1

ADD docker-requirements.txt docker-requirements.txt

RUN pip install -r docker-requirements.txt

ENV TORCH_HOME=/workspace/disco-diffusion-1/models

# Clone Git repositories
RUN git clone $REPO
WORKDIR /workspace/disco-diffusion-1
RUN pip install jupyterlab
RUN echo 'export PATH="$HOME/.local/bin:$HOME/.local/bin/jupyter-lab:$PATH"' >> ~/.bashrc
USER root
RUN pip install jupyterlab
RUN echo 'export PATH="$HOME/.local/bin:$HOME/.local/bin/jupyter-lab:$PATH"' >> ~/.bashrc
USER disco
ADD start.sh /start.sh
CMD [ "/start.sh" ]