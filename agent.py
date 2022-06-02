import math
from pkgutil import extend_path
import subprocess
from time import sleep
from loguru import logger
import requests
import json
import argparse
import os
from dotenv import load_dotenv
import time
import traceback


def loop(args=None):
    DD_URL = args.dd_url
    DD_NAME = args.agent
    DD_IMAGES_OUT = args.images_out
    DD_CUDA_DEVICE = args.cuda_device
    POLL_INTERVAL = args.poll_interval
    idle_time = 0
    run = True
    while run == True:
        connected = False
        url = f"{DD_URL}/takeorder/{DD_NAME}/{idle_time}"
        try:
            logger.debug(f"🌎 Checking '{url}'")
            results = requests.get(url).json()
            if results["success"]:
                idle_time = 0
                connected = True
                print(results["details"])
                tp = results["details"]["text_prompt"]
                tp = tp.replace("“", '"')
                tp = tp.replace("”", '"')
                # Attempt to accept JSON Structured Text Prompt...
                try:
                    tp = eval(tp)
                    if type(tp) == list:
                        prompt = json.dumps({0: tp})
                        logger.info("JSON structured text prompt found.")
                    else:
                        raise Exception("Non-list item found")
                except:
                    tp = results["details"]["text_prompt"]
                    tp = tp.replace(":", "")
                    tp = tp.replace('"', "")
                    prompt = json.dumps({0: [tp]})
                    logger.info("Flat string text prompt found.")
                steps = results["details"]["steps"]
                uuid = results["details"]["uuid"]
                shape = results["details"]["shape"]
                model = results["details"]["model"]
                clamp_max = results["details"]["clamp_max"]
                clip_guidance_scale = results["details"]["clip_guidance_scale"]
                cut_ic_pow = results["details"]["cut_ic_pow"]
                sat_scale = results["details"]["sat_scale"]
                try:
                    render_type = results["details"]["render_type"]
                except:
                    render_type = "render"
                try:
                    set_seed = results["details"]["set_seed"]
                except:
                    set_seed = "random_seed"
                try:
                    symmetry = results["details"]["symmetry"]
                except:
                    symmetry = "no"
                try:
                    symmetry_loss_scale = results["details"]["symmetry_loss_scale"]
                except:
                    symmetry_loss_scale = 1500

                if set_seed == -1:
                    set_seed = "random_seed"

                print(results["details"])
                w_h = [1280, 768]
                RN101 = False
                RN50 = True
                RN50x16 = False
                RN50x4 = False
                RN50x64 = False
                ViTB16 = True
                ViTB32 = True
                ViTL14 = False
                ViTL14_336 = False

                if not clamp_max:
                    clamp_max = 0.05

                if not clip_guidance_scale:
                    clip_guidance_scale = 1500

                if not cut_ic_pow:
                    cut_ic_pow = 1

                if not sat_scale:
                    sat_scale = 0

                if not model:
                    model = "default"

                if model == "rn50x64":
                    RN50x64 = True
                    RN50 = False

                if model == "vitl14":
                    RN50 = False
                    ViTL14 = True

                if model == "vitl14x336":
                    RN50 = False
                    ViTL14_336 = True

                if not shape:
                    shape = "landscape"

                if render_type == "sketch":
                    if shape == "landscape":
                        w_h = [640, 512]
                    if shape == "portrait":
                        w_h = [512, 640]
                    if shape == "square":
                        w_h = [512, 512]
                    if shape == "pano":
                        w_h = [1024, 256]
                else:
                    if shape == "landscape":
                        w_h = [1280, 768]
                    if shape == "portrait":
                        w_h = [768, 1280]
                    if shape == "square":
                        w_h = [1024, 1024]
                    if shape == "pano":
                        w_h = [2048, 512]

                job = f"python disco.py --dd_bot=true --dd_bot_url={DD_URL} --dd_bot_agentname={DD_NAME} --batch_name={uuid} --display_rate=5 --set_seed={set_seed} --cuda_device={DD_CUDA_DEVICE} --n_batches=1 --images_out={DD_IMAGES_OUT} --steps={steps} --clamp_max={clamp_max} --clip_guidance_scale={clip_guidance_scale} --cut_ic_pow={cut_ic_pow} --sat_scale={sat_scale} --text_prompts"
                cmd = job.split(" ")
                cmd.append(f"{prompt}")
                cmd.append(f"--width_height")
                cmd.append(json.dumps(w_h))
                cmd.append(f"--RN101")
                cmd.append(str(RN101))
                cmd.append(f"--RN50")
                cmd.append(str(RN50))
                cmd.append(f"--RN50x4")
                cmd.append(str(RN50x4))
                cmd.append(f"--RN50x16")
                cmd.append(str(RN50x16))
                cmd.append(f"--RN50x64")
                cmd.append(str(RN50x64))
                cmd.append(f"--ViTB16")
                cmd.append(str(ViTB16))
                cmd.append(f"--ViTB32")
                cmd.append(str(ViTB32))
                cmd.append(f"--ViTL14")
                cmd.append(str(ViTL14))
                cmd.append(f"--ViTL14_336")
                cmd.append(str(ViTL14_336))
                if symmetry == "yes":
                    cmd.append(f"--symmetry_loss")
                    cmd.append(str(True))
                    cmd.append(f"--symmetry_switch")
                    cmd.append(str(math.floor(int(steps) / 2)))
                    cmd.append(f"--symmetry_loss_scale")
                    cmd.append(str(symmetry_loss_scale))
                print(cmd)
                logger.info(f"Running...:\n{job}")
                s = time.time()
                log = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")
                e = time.time()
                duration = e - s
                files = {"file": open(f"{DD_IMAGES_OUT}/{uuid}/{uuid}(0)_0.png", "rb")}
                values = {"duration": duration}
                r = requests.post(f"{DD_URL}/upload/{DD_NAME}/{uuid}", files=files, data=values)
                files = {"file": open(f"{DD_IMAGES_OUT}/{uuid}/{uuid}(0).log", "rb")}
                r = requests.post(f"{DD_URL}/uploadlog/{DD_NAME}/{uuid}", files=files, data=values)
            else:
                logger.info(f"{results['message']}")
        except KeyboardInterrupt:
            logger.info("Exiting...")
            run = False
        except Exception as e:
            if connected:
                tb = traceback.format_exc()
                logger.error(f"Bad job detected.\n\n{e}")
                values = {"message": f"Job failed:\n\n{e}", "traceback": tb, "log": log}
                r = requests.post(f"{DD_URL}/reject/{DD_NAME}/{uuid}", data=values)
            else:
                logger.error(f"Error.  Check your DD_URL and if the DD app is running at that location.  Also check your own internet connectivity.  Exception:\n{e}")
        finally:
            logger.info(f"Sleeping for {POLL_INTERVAL} seconds...  I've been sleeping for {idle_time} seconds.")
            idle_time = idle_time + POLL_INTERVAL
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
