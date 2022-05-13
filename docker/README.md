# Docker

## Introduction

This is a Docker build file that will preinstall dependencies, packages, Git repos, and allow mounting and persisting pre-downloaded large model files needed by Disco Diffusion.

## Change Log

- `2.0`
  Completely change Docker Image Setup

- `1.1`

  Added support for passing parameters via environment variables

- `1.0`

  Initial build file created based on the DD 5.1 Git repo.  This initial build is deliberately meant to work touch-free of any of the existing Python code written.  It does handle some of the pre-setup tasks already done in the Python code such as pip packages, Git clones, and even pre-caching the model files for faster launch speed.

## Build the Image

From a terminal in the `docker` directory, run:

```sh
docker build -t disco-diffusion .
```
## Create some volumes

```sh
mkdir -p /disco-diffusion/images_out
mkdir -p /disco-diffusion/init_images
mkdir -p /disco-diffusion/models
mkdir -p /disco-diffusion/configs
```

## Run a Test Job

This example runs Disco Diffusion in a Docker container.  It maps 4 volumes (`images_out`, `init_images`, `configs`, and `models`) to the container.  It runs with all default parameters for sake of a barebones example.  Press Control+C to terminate the run after confirming your test run works.

```sh
docker run --rm -it \
    -v $(echo ~)/disco-diffusion/images_out:/workspace/code/images_out \
    -v $(echo ~)/disco-diffusion/init_images:/workspace/code/init_images \
    -v $(echo ~)/disco-diffusion/models:/workspace/disco-diffusion-1/models \
    -v $(echo ~)/disco-diffusion/configs:/workspace/disco-diffusion/configs \
    --gpus=all \
    --name="disco-diffusion" --ipc=host \
    --user $(id -u):$(id -g) \
disco-diffusion python disco.py
```

## Passing Parameters

- Parameters can be optionally specified with:
  - Environment variables passed to the Docker Container
  - Command-Line arguments (use `--help` to get a list)
- YAML files can now also be used.  See parameter `--config_file`
- Examples to come.

