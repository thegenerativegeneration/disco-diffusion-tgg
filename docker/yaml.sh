sudo docker pull thegenerativegeneration/disco-diffusion-tgg
sudo docker stop disco-yaml
sudo docker run --rm -it \
    -p 8888:8888 \
    -v $(echo ~)/disco-diffusion/images_out:/workspace/disco-diffusion-tgg/images_out \
    -v $(echo ~)/disco-diffusion/init_images:/workspace/disco-diffusion-tgg/init_images \
    -v $(echo ~)/disco-diffusion/models:/workspace/disco-diffusion-tgg/models \
    -v $(echo ~)/disco-diffusion/configs:/workspace/disco-diffusion-tgg/configs \
    --gpus=all \
    --name="disco-yaml" --ipc=host \
    --user $(id -u):$(id -g) \
thegenerativegeneration/disco-diffusion-tgg python disco.py --config_file=$1