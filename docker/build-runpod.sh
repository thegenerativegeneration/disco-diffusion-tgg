docker build -t entmike/disco-diffusion-1:runpod \
    --build-arg model_path=\/models \
    --build-arg base_image=entmike/disco-diffusion-1:basemodels \
    --build-arg DD_VERSION=2.5.runpod \
    -f Dockerfile .