sudo docker pull entmike/disco-diffusion-1
sudo docker stop disco-yaml
sudo docker run --rm -it \
    -p 8888:8888 \
    -v $(echo ~)/disco-diffusion/images_out:/workspace/disco-diffusion-1/images_out \
    -v $(echo ~)/disco-diffusion/init_images:/workspace/disco-diffusion-1/init_images \
    -v $(echo ~)/disco-diffusion/models:/workspace/disco-diffusion-1/models \
    -v $(echo ~)/disco-diffusion/configs:/workspace/disco-diffusion-1/configs \
    --gpus=all \
    --name="disco-yaml" --ipc=host \
    --user $(id -u):$(id -g) \
entmike/disco-diffusion-1 python disco.py --config_file=$1