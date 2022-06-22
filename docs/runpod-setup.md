# Prerequisites

  - A RunPod account
  - Money

## Setup

1. Visit the [RunPod Website](https://runpod.io/).
2. Click 'Secure Cloud'
3. You will be presented with different machine types.  Select the desired type, and click **Select**.
4. Under **Select a Template**, choose **Disco Diffusion**
5. Click **Ok**
6. Click **Continue**
7. Click **Deploy Spot** or **Deploy On-Demand** depending on your preference.
  (spot instances are cheap, but interruptable | on-demand instances are more expensive but non-interruptible)
9. A modal popup will appear, click **My Pods**
10. Click **Connect** and then click **Connect To Jupyter**
11. You are now in Jupyter Notebook within the RunPod Docker Container `entmike/disco-diffusion-1`!  Things may look familiar to you.
12. In JupyterLab, Click **Terminal**
13. Do a test run with `python disco.py`
14. Look at your pretty images in `images_out` start to develop.

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

Unlike the Lambda Labs guide, at this point you do NOT have to type `sudo docker ...` commands.  All commands simply begin with `python disco.py` followed by any command-line arguments you wish to pass (or `--config_file=path/to/your/config.yaml`) for YAML args.
