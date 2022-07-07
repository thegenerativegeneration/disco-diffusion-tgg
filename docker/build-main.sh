docker build -t thegenerativegeneration/disco-diffusion-tgg \
    --build-arg model_path=/workspace/disco-diffusion-tgg/models \
    --build-arg base_image=pytorch/pytorch \
    --build-arg DD_VERSION=2.5 \
    -f Dockerfile .