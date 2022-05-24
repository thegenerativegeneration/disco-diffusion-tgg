import subprocess
from time import sleep
from loguru import logger
import requests
import json
import argparse
import os
from dotenv import load_dotenv


def loop(args=None):
    DD_URL = args.dd_url
    DD_NAME = args.agent
    DD_IMAGES_OUT = args.images_out
    DD_CUDA_DEVICE = args.cuda_device
    POLL_INTERVAL = args.poll_interval

    url = f"{DD_URL}/takeorder/{DD_NAME}"
    run = True
    while run == True:
        try:
            logger.debug(f"🌎 Checking '{url}'")
            results = requests.get(url).json()
            if results["success"]:
                prompt = json.dumps({0: [results["details"]["text_prompt"]]})
                steps = results["details"]["steps"]
                uuid = results["details"]["uuid"]
                job = f"python disco.py --batch_name={uuid} --cuda_device={DD_CUDA_DEVICE} --n_batches=1 --images_out={DD_IMAGES_OUT} --steps={steps} --text_prompts"
                cmd = job.split(" ")
                cmd.append(f"{prompt}")
                print(cmd)
                # logger.info(f"Running...:\n{job}")
                log = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")
                logger.info(log)
                files = {"file": open(f"{DD_IMAGES_OUT}/{uuid}/{uuid}(0)_0.png", "rb")}
                values = {}
                r = requests.post(f"{DD_URL}/upload/{DD_NAME}/{uuid}", files=files, data=values)
            else:
                logger.error(f"Error: {results['message']}")
        except KeyboardInterrupt:
            logger.info("Exiting...")
            run = False
        except:
            logger.error("Error.  Check your DD_URL and if the DD app is running at that location.  Also check your own internet connectivity.")
        finally:
            logger.info(f"Sleeping for {POLL_INTERVAL} seconds...")
            sleep(POLL_INTERVAL)


def main():

    load_dotenv()
    parser = argparse.ArgumentParser(description="Disco Diffusion")
    parser.add_argument("--dd_url", help="Discord Bot http endpoint", required=False, default=os.getenv("DD_URL"))
    parser.add_argument("--agent", help="Your agent name", required=False, default=os.getenv("DD_NAME"))
    parser.add_argument("--images_out", help="Directory for render jobs", required=False, default=os.getenv("DD_IMAGES_OUT", "images_out"))
    parser.add_argument("--cuda_device", help="CUDA Device", required=False, default=os.getenv("DD_CUDA_DEVICE", "cuda:0"))
    parser.add_argument("--poll_interval", type=int, help="Polling interval between jobs", required=False, default=os.getenv("DD_POLL_INTERVAL", 5))
    args = parser.parse_args()
    loop(args)


if __name__ == "__main__":
    main()
