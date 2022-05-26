# Prerequisites

  - A RunPod account
  - Money

## Setup

1. Visit the [RunPod Website](https://runpod.io/).
2. Click 'Secure Cloud'
3. You will be presented with different machine types.  Select the desired type, and click **Select**.
4. Under **Select a Template**, choose **Custom Container**
5. For **Container Disk**, leave at `40GB`
6. For **Volume Disk**, change to `50GB`
7. Next, click **Customize Deployment**
8. For **Docker Image Name**, change to `entmike/disco-diffusion-1`
9. For **Pod Name**, call it whatever you want.
10. For **Docker Command**, change to `jupyter lab --NotebookApp.allow_origin="*" --NotebookApp.token=yourpassword`
11. For **Expose HTTP Port**, change to `8888`
12. For **Expose TCP Port**, change to `80`
13. Click **Ok**
14. Click **Continue**
15. Click **Deploy Spot** or **Deploy On-Demand** depending on your preference.
16. A modal popup will appear, click **My Pods**
17. Click **Connect** and then click **Connect via HTTP**
18. You will be prompted to enter your token/password.  Use the password you specified in **Step 10** above.
19. You are now in Jupyter Notebook within the RunPod Docker Container `entmike/disco-diffusion-1`!  Things may look familiar to you.

## Commands

### Run a batch from YAML

`python disco.py --config_file=configs/xyz.yaml`

### ZIP a folder

`zip -r downloads.zip images_out/batchname`

## Notes

Unlike the Lambda Labs guide, at this point you do NOT have to type `sudo docker ...` commands.  All commands simply begin with `python discord.py` followed by any command-line arguments you wish to pass (or `--config_file=path/to/your/config.yaml`) for YAML args.
