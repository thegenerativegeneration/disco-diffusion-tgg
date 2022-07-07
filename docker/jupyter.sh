sudo docker stop disco-jupyter
sudo docker run --rm -it \
    -p 8888:8888 \
    -v $(echo ~)/disco-diffusion/images_out:/workspace/disco-diffusion-tgg/images_out \
    -v $(echo ~)/disco-diffusion/init_images:/workspace/disco-diffusion-tgg/init_images \
    -v $(echo ~)/disco-diffusion/models:/workspace/disco-diffusion-tgg/models \
    -v $(echo ~)/disco-diffusion/configs:/workspace/disco-diffusion-tgg/configs \
    --gpus=all \
    --name="disco-jupyter" --ipc=host \
    --user $(id -u):$(id -g) \
thegenerativegeneration/disco-diffusion-tgg jupyter lab --ip 0.0.0.0 --NotebookApp.token='' --NotebookApp.password=''
