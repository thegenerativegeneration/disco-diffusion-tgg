import json

import os, sys
import subprocess, torch
import dd, dd_args
import random
from pydotted import pydot
import base64

args = pydot({})
import ipywidgets as widgets
from IPython.display import display, Markdown

# @markdown Leave these as defaults unless you know what you are doing.

# print("Loading, please wait...")

content_root = "/content"
cwd = os.path.abspath(".")
is_local = True

if is_local:
    content_root = cwd
# print(f"Current directory: {cwd}")

dd_root = f"{content_root}"

# print(f'✅ Disco Diffusion root path will be "{dd_root}"')

root_path = dd_root

os.chdir(f"{dd_root}")


# Downgrade for T4/V100
device_name = torch.cuda.get_device_name(0)
# print(f"🔍 You have a {device_name} GPU.")
if "V100" in device_name or "T4" in device_name:
    print(f"⚠️ {torch.cuda.get_device_name(0)} detected.  Do not use ViTL14 or ViTL14@336 models...")

# Set base project directory to current working directory
PROJECT_DIR = dd_root

sys.path.append(PROJECT_DIR)

# Unsure about these:
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# import warnings
# warnings.filterwarnings("ignore", category=UserWarning)

# print(dd.is_in_notebook())

config_file = open("configs/dd_gui.yaml", "r")

config_file_input = widgets.Textarea(
    value=config_file.read(),
    disabled=False,
    layout={"width": "100%", "height": "500px"},
)

display(config_file_input)

def run_dd(out):
    with out:
        with open("./configs/dd_gui.yaml", "w") as config_file_new:
            config_file_new.write(config_file_input.value)
        
        pargs = dd_args.arg_configuration_loader({
            "config_file":'/workspace/disco-diffusion-1/configs/dd_gui.yaml'
        })
        
        # Setup folders
        folders = dd.setupFolders(is_colab=dd.detectColab(), PROJECT_DIR=PROJECT_DIR, pargs=pargs)

        # Report System Details
        dd.systemDetails(pargs)

        # Get CUDA Device
        device = dd.getDevice(pargs)

        dd.start_run(pargs=pargs, folders=folders, device=device, is_colab=dd.detectColab())

