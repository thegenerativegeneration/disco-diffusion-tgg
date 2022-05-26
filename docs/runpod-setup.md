# Prerequisites

  - A RunPod account
  - Money

## Setup

1. Visit the [RunPod Website](https://runpod.io/).
2. Click 'Secure Cloud'
3. You will be presented with different machine types.  Select the desired type, and click **Select**.
4. Under **Select a Template**, choose **Custom Container**
5. Next, click **Customize Deployment**
6. For **Docker Image Name**, change to `entmike/disco-diffusion-1`
7. For **Pod Name**, call it whatever you want.
8. At the bottom, expand **Environment Variables**, and set `JUPYTER_PASSWORD` to a password you want.
9. For **Expose HTTP Port**, change to `8888`
10. Click **Ok**
11. Click **Continue**
12. Click **Deploy Spot** or **Deploy On-Demand** depending on your preference.
13. A modal popup will appear, click **My Pods**
14. Click **Connect** and then click **Connect via HTTP**
15. You will be prompted to enter your token/password.  Use the password you specified in **Step 8** above.
16. You are now in Jupyter Notebook within the RunPod Docker Container `entmike/disco-diffusion-1`!  Things may look familiar to you.
17. In JupyterLab, Click **Terminal**
18. Do a test run with `python disco.py`
19. Look at your pretty images in `images_out` start to develop.

## Example Commands

### Get Help

`python disco.py --help`

### Simple Command Line arguments run

`python disco.py --steps 350 --batch_name=simple-example --text_prompts='{"0":["a pretty sailboat floating in the ocean in front of a colorful sunset, trending on artstation"]}'`

### Run a batch from YAML

`python disco.py --config_file=configs/xyz.yaml`

### ZIP a folder

`zip -r downloads.zip images_out/batchname`

## Notes

Unlike the Lambda Labs guide, at this point you do NOT have to type `sudo docker ...` commands.  All commands simply begin with `python discord.py` followed by any command-line arguments you wish to pass (or `--config_file=path/to/your/config.yaml`) for YAML args.
