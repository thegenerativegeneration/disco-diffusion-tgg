docker build -t entmike/disco-diffusion-1 \
    --build-arg model_path=models \
    --build-arg base_image=pytorch/pytorch \
    --build-arg DD_VERSION=2.5 \
    -f Dockerfile .