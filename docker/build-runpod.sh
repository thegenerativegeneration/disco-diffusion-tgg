docker build -t thegenerativegeneration/disco-diffusion-tgg:runpod \
    --build-arg model_path=\/models \
    --build-arg base_image=thegenerativegeneration/disco-diffusion-tgg:basemodels \
    --build-arg DD_VERSION=2.5.runpod \
    -f Dockerfile .