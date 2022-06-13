import json

import os, sys
import subprocess, torch
import dd, dd_args
import random
from pydotted import pydot

args = pydot({})
import ipywidgets as widgets
from IPython.display import display, Markdown

# @markdown Leave these as defaults unless you know what you are doing.

print("Loading, please wait...")

content_root = "/content"
cwd = os.path.abspath(".")
is_local = True

if is_local:
    content_root = cwd
print(f"Current directory: {cwd}")

dd_root = f"{content_root}"

print(f'✅ Disco Diffusion root path will be "{dd_root}"')

root_path = dd_root

os.chdir(f"{dd_root}")


# Downgrade for T4/V100
device_name = torch.cuda.get_device_name(0)
print(f"🔍 You have a {device_name} GPU.")
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

params = []


def make_widget(widget, label, checkbox=False):
    params.append({"widget": widget, "key": label})
    if label:
        if checkbox:
            return widgets.HBox([widget, widgets.Label(label)])
        else:
            return widgets.HBox([widgets.Label(value=label, layout=widgets.Layout(width="150px")), widget])

    else:
        return widget


# DEFAULTS

# @markdown ##💡Batch/Config Parameters

batch_name = make_widget(widgets.Text(value="TimeToDisco", disabled=False), "batch_name")

resume_run = make_widget(
    widgets.Checkbox(
        value=False,
        indent=False,
    ),
    "resume_run",
    True,
)

run_to_resume = make_widget(
    widgets.Text(
        value="latest",
    ),
    "run_to_resume",
)

retain_overwritten_frames = make_widget(
    widgets.Checkbox(
        value=False,
        indent=False,
    ),
    "retain_overwritten_frames",
    True,
)

batch_tab = widgets.VBox([batch_name, resume_run, run_to_resume, retain_overwritten_frames])

# @markdown ## 🔍Preview Settings

intermediate_saves = make_widget(
    widgets.IntText(
        value=0,
    ),
    "intermediate_saves",
)

intermediates_in_subfolder = make_widget(
    widgets.Checkbox(
        value=True,
        indent=False,
    ),
    "intermediates_in_subfolder",
    True,
)

console_preview = make_widget(
    widgets.Checkbox(
        value=True,
        indent=False,
    ),
    "console_preview",
    True,
)

console_preview_width = make_widget(
    widgets.IntText(
        value=80,
    ),
    "console_preview_width",
)

display_rate = make_widget(
    widgets.IntText(
        value=50,
    ),
    "display_rate",
)

config_file = make_widget(
    widgets.Text(
        value=None,
    ),
    "config_file",
)

n_batches = make_widget(
    widgets.IntText(
        value=150,
    ),
    "n_batches",
)

preview_tab = widgets.VBox([intermediate_saves, intermediates_in_subfolder, console_preview, console_preview_width, display_rate, config_file, n_batches])

args.prompt_salad = False  # @param {type:"boolean"}
# @markdown Your text prompt mixing template.  Each `{placeholder}` represents an "ingredient" in your salad that will draw from a text file in `prompt_salad/`  You can even add a sub-folder such as `{scifi/artists}` which will resolve to filename `{prompt_salad/scifi/artists.txt}` for any personal customizations!
args.prompt_salad_template = "{colors} {things} in the {custom/customword} shape of {shapes}, art by {artists}"  # @param
# @markdown How many prompt salads to generate
args.prompt_salad_amount = 5  # @param {type:"number"}
args.fuzzy_prompt = False  # @param {type:"boolean"}


# @markdown ## 🖼️ Init Image Settings

init_image = make_widget(widgets.Text(value=None), "init_image")

init_scale = make_widget(
    widgets.IntText(
        value=1000,
    ),
    "init_scale",
)

skip_steps = make_widget(
    widgets.IntText(
        value=0,
    ),
    "skip_steps",
)

init_image_tab = widgets.VBox(
    [
        init_image,
        init_scale,
        skip_steps,
    ]
)

# @markdown ## 💥 Perlin/Voronoi Settings

init_generator = make_widget(
    widgets.Dropdown(
        options=["perlin", "voronoi"],
        value="perlin",
        disabled=False,
    ),
    "init_generator",
)

perlin_init = make_widget(
    widgets.Checkbox(
        value=False,
        indent=False,
    ),
    "perlin_init",
    True,
)

perlin_mode = make_widget(
    widgets.Dropdown(
        options=["mixed", "color", "gray"],
        value="mixed",
    ),
    "perlin_mode",
)

voronoi_points = make_widget(
    widgets.Dropdown(
        options=[20, 50, 100, 150, 250, 500, 1000],
        value=20,
    ),
    "voronoi_points",
)

voronoi_palette = make_widget(widgets.Text(value="default.yaml"), "voronoi_palette")

perlin_voronoi_tab = widgets.VBox([init_generator, perlin_init, perlin_mode, voronoi_points, voronoi_palette])

# @markdown ## 🧪 (Experimental) Target Image Settings
# @markdown Warning: work in progress!
args.target_image = None  # @param {type:"raw"}
args.target_scale = 20000  # @param {type:"number"}

# @markdown ## ✂️ CLIP settings

cutn_batches = make_widget(
    widgets.IntText(
        value=4,
    ),
    "cutn_batches",
)
clip_guidance_scale = make_widget(
    widgets.IntText(
        value=5000,
    ),
    "clip_guidance_scale",
)
cut_overview = make_widget(widgets.Text(value="[12]*400+[4]*600"), "cut_overview")
cut_innercut = make_widget(widgets.Text(value="[4]*400+[12]*600"), "cut_innercut")
cut_icgray_p = make_widget(widgets.Text(value="[0.2]*400+[0]*600"), "cut_icgray_p")
cut_ic_pow = make_widget(
    widgets.FloatText(
        value=1,
    ),
    "cut_ic_pow",
)
eta = make_widget(
    widgets.FloatText(
        value=0.8,
    ),
    "eta",
)
clamp_max = make_widget(
    widgets.FloatText(
        value=0.05,
    ),
    "clamp_max",
)

rand_mag = make_widget(
    widgets.FloatText(
        value=0.05,
    ),
    "rand_mag",
)

tv_scale = make_widget(
    widgets.IntText(
        value=0,
    ),
    "tv_scale",
)

range_scale = make_widget(
    widgets.IntText(
        value=150,
    ),
    "range_scale",
)

sat_scale = make_widget(
    widgets.FloatText(
        value=0,
    ),
    "sat_scale",
)

clamp_grad = make_widget(
    widgets.Checkbox(
        value=True,
        indent=False,
    ),
    "clamp_grad",
    True,
)
clip_denoised = make_widget(
    widgets.Checkbox(
        value=False,
        indent=False,
    ),
    "clip_denoised",
    True,
)
skip_augs = make_widget(
    widgets.Checkbox(
        value=False,
        indent=False,
    ),
    "skip_augs",
    True,
)

clip_tab = widgets.VBox(
    [
        cutn_batches,
        clip_guidance_scale,
        cut_overview,
        cut_innercut,
        cut_icgray_p,
        cut_ic_pow,
        eta,
        clamp_max,
        rand_mag,
        tv_scale,
        range_scale,
        sat_scale,
        clamp_grad,
        clip_denoised,
        skip_augs,
    ]
)

# @markdown ## 🎞️ Animation Settings

animation_mode = make_widget(
    widgets.Dropdown(
        options=["None", "2D", "3D", "Video Input"],
        value="None",
    ),
    "animation_mode",
)

args.video_init_path = "training.mp4"  # @param {type:"string"}
args.extract_nth_frame = 10  # @param {type:"number"}
args.video_init_seed_continuity = True  # @param {type:"boolean"}
args.key_frames = True  # @param {type:"boolean"}
args.max_frames = 10000  # @param {type:"number"}
args.interp_spline = "Linear"  # @param ["Linear", "Quadratic", "Cubic"]
args.frames_skip_steps = "60%"  # @param {type:"string"}
args.vr_mode = False  # @param {type:"boolean"}
args.angle = "0:(0)"  # @param {type:"string"}
args.zoom = "0:(1),10:(1.05)"  # @param {type:"string"}
args.translation_x = "0: (0)"  # @param {type:"string"}
args.translation_y = "0: (0)"  # @param {type:"string"}
args.translation_z = "0: (10.0)"  # @param {type:"string"}
args.rotation_3d_x = "0: (0)"  # @param {type:"string"}
args.rotation_3d_y = "0: (0)"  # @param {type:"string"}
args.rotation_3d_z = "0: (0)"  # @param {type:"string"}
args.midas_depth_model = "dpt_large"  # @param {type:"string"}
args.midas_weight = 0.3  # @param {type:"number"}
args.near_plane = 0  # @param {type:"number"}
args.far_plane = 0  # @param {type:"number"}
args.fov = 0  # @param {type:"number"}
args.padding_mode = "border"  # @param {type:"string"}
args.sampling_mode = "bicubic"  # @param {type:"string"}
args.turbo_mode = False  # @param {type:"boolean"}
args.turbo_steps = 3  # @param {type:"number"}
args.turbo_preroll = 10  # @param {type:"number"}
args.frames_scale = 1500  # @param {type:"number"}
args.frames_skip_steps = "60%"  # @param {type:"string"}

# @markdown ### 🔽 Vertical Symmetry Settings (experimental)
args.v_symmetry_loss = False  # @param {type:"boolean"}
args.v_symmetry_loss_scale = 1500  # @param {type:"number"}
args.v_symmetry_switch = 80  # @param {type:"number"}
# @markdown ### 📱 Twilio SMS Settings (Optional)
# @markdown Tired of babysitting your jobs?  Get a text message to your phone!  See [Twilio](https://www.twilio.com/) site for more info.
args.twilio_account_sid = ""  # @param {"type":"string"}
args.twilio_auth_token = ""  # @param {"type":"string"}
args.twilio_from = ""  # @param {"type":"string"}
args.twilio_to = ""  # @param {"type":"string"}
# @markdown ### ⚙️ Batching and DB Settings
args.modifiers = {}  # @param type="raw"
args.multipliers = {}  # @param type="raw"
args.save_metadata = False  # @param {type:"boolean"}
args.db = "/content/gdrive/MyDrive/disco-diffusion-1/disco.db"  # @param {"type":"string"}


# @markdown ### ⚙️ Appendix
# @markdown Lesser used options
# @markdown
# @markdown **`init_images`** specifies the base `init_images` folder to look for any (optional) init images.
args.init_images = "init_images"  # @param {type:"string"}
# @markdown **`init_images`** specifies the base `images_out` folder to look for your batch output
args.images_out = "images_out"  # @param {type:"string"}
# @markdown **`model_path`** specifies the folder where your models are downloaded to and used
args.model_path = json.loads(os.getenv("model_path", '"models"'))  # @param {type:"string"}
# prompt_salad_path Specifies base prompt_salad paths.
args.prompt_salad_path = "prompt_salad"
args.cuda_device = "cuda:0"
# @markdown **`gen_config`** specifies the name of the generated YAML configuration file that will be saved in `configs` folder.  `AUTO` means the file will be `[batch_name]_gen.yaml` will be used.
args.gen_config = "AUTO"  # @param {type:"string"}
# @markdown **`gen_config_only`** indicates the configuration only will be generated, and no batch will run.
args.gen_config_only = False  # @param {type:"boolean"}
args.use_checkpoint = True  # @param {type:"boolean"}
args.cutout_debug = False  # @param {type:"boolean"}
args.google_drive = False
# @markdown image_prompts are supported but are not good.
args.image_prompts = {}  # @param type="raw"


text_prompts_input = widgets.Textarea(
    value='{"0": ["A beautiful painting of a singular lighthouse, shining its light across a tumultuous sea of blood by greg rutkowski and thomas kinkade, Trending on artstation.","yellow color scheme"],"100": ["This set of prompts start at frame 100","This prompt has weight five:5"]}',
    disabled=False,
    layout={"width": "600px", "height": "300px"},
)

text_prompts = make_widget(text_prompts_input, "text_prompts")

prompt_salad = make_widget(
    widgets.Checkbox(
        value=False,
        indent=False,
    ),
    "prompt_salad",
    True,
)

prompt_salad_amount = make_widget(
    widgets.IntText(
        value=5,
    ),
    "prompt_salad_amount",
)

prompt_salad_template = make_widget(
    widgets.Textarea(value="{colors} {things} in the {custom/customword} shape of {shapes}, art by {artists}", layout=widgets.Layout(width="600px")), "prompt_salad_template"
)

fuzzy_prompt = make_widget(
    widgets.Checkbox(
        value=False,
        indent=False,
    ),
    "fuzzy_prompt",
    True,
)

heightInput = widgets.BoundedIntText(value=768, min=100, max=10000, step=1, disabled=False)

height = make_widget(heightInput, "height")

widthInput = widgets.BoundedIntText(value=1280, min=100, max=10000, step=1, disabled=False)

width = make_widget(widthInput, "width")

steps = make_widget(widgets.BoundedIntText(value=250, min=1, max=1000, step=1, disabled=False), "steps")

RN50 = make_widget(widgets.Checkbox(value=True, disabled=False, indent=False, layout=widgets.Layout(width="20px")), "RN50", True)

RN101 = make_widget(widgets.Checkbox(value=False, disabled=False, indent=False, layout=widgets.Layout(width="20px")), "RN101", True)

RN50x64 = make_widget(widgets.Checkbox(value=False, disabled=False, indent=False, layout=widgets.Layout(width="20px")), "RN50x64", True)

RN50x16 = make_widget(widgets.Checkbox(value=False, disabled=False, indent=False, layout=widgets.Layout(width="20px")), "RN50x16", True)

RN50x4 = make_widget(widgets.Checkbox(value=False, disabled=False, indent=False, layout=widgets.Layout(width="20px")), "RN50x4", True)

ViTB16 = make_widget(widgets.Checkbox(value=True, disabled=False, indent=False, layout=widgets.Layout(width="20px")), "ViTB16", True)

ViTB32 = make_widget(widgets.Checkbox(value=True, disabled=False, indent=False, layout=widgets.Layout(width="20px")), "ViTB32", True)

ViTL14 = make_widget(widgets.Checkbox(value=False, disabled=False, indent=False, layout=widgets.Layout(width="20px")), "ViTL14", True)

ViTL14_336 = make_widget(widgets.Checkbox(value=False, disabled=False, indent=False, layout=widgets.Layout(width="20px")), "ViTL14_336", True)

use_secondary_model = make_widget(widgets.Checkbox(value=True, disabled=False, indent=False, layout=widgets.Layout(width="20px")), "use_secondary_model", True)

randomize_class = make_widget(widgets.Checkbox(value=True, disabled=False, indent=False, layout=widgets.Layout(width="20px")), "randomize_class", True)

diffusion_model = make_widget(
    widgets.Dropdown(
        options=["512x512_diffusion_uncond_finetune_008100", "256x256_diffusion_uncond"],
        value="512x512_diffusion_uncond_finetune_008100",
        disabled=False,
    ),
    "diffusion_model",
)

diffusion_sampling_mode = make_widget(
    widgets.Dropdown(
        options=["ddim", "plms"],
        value="ddim",
        disabled=False,
    ),
    "diffusion_sampling_mode",
)

clip_guidance_scale = make_widget(widgets.BoundedIntText(value=5000, min=0, max=30000, step=1, disabled=False), "clip_guidance_scale")

symmetry_loss = make_widget(widgets.Checkbox(value=False, disabled=False, indent=False, layout=widgets.Layout(width="20px")), "symmetry_loss", True)

symmetry_loss_scale = make_widget(
    widgets.IntText(
        value=1500,
    ),
    "symmetry_loss_scale",
)

symmetry_switch = make_widget(widgets.IntText(value=80), "symmetry_switch")

symmetry_tab = widgets.VBox([symmetry_loss, symmetry_loss_scale, symmetry_switch])

cuda_device = make_widget(widgets.Text(value="cuda:0", disabled=False), "cuda_device")

set_seed_input = widgets.Text(value="random_seed", disabled=False)

set_seed = make_widget(set_seed_input, "set_seed")

basic_tab = widgets.VBox([text_prompts, steps, height, width, set_seed, cuda_device])
model_tab = widgets.VBox(
    [RN50, RN101, RN50x64, RN50x16, RN50x4, ViTB16, ViTB32, ViTL14, ViTL14_336, use_secondary_model, diffusion_model, diffusion_sampling_mode, randomize_class]
)

children = [basic_tab, model_tab, clip_tab, symmetry_tab, preview_tab, init_image_tab, perlin_voronoi_tab]
tab = widgets.Tab()
tab.children = children
titles = ["Basic Options", "Model", "Clip", "Symmetry", "Preview", "Init Image", "Perlin/Voronoi"]
[tab.set_title(i, title) for i, title in enumerate(titles)]
display(tab)

button = widgets.Button(
    description="Start Run", disabled=False, button_style="success", icon="check"  # 'success', 'info', 'warning', 'danger' or ''  # (FontAwesome names without the `fa-` prefix)
)

display(button)

image_display = widgets.Output()
display(image_display)

out = widgets.Output(layout={"border": "1px solid black"})

display(out)


def run_dd(button=None):
    with out:
        for param in params:
            argKey = param["key"]
            args[argKey] = param["widget"].value

        try:
            args.text_prompts = json.loads(text_prompts_input.value)
        except:
            print("text prompts must be valid json")

        args.width_height = [widthInput.value, heightInput.value]

        args.set_seed = set_seed_input.value

        dd_args.arg_configuration_loader()  # Workaround to do param saving to yaml for now.
        pargs = args  # Dont run through arg_configuration_loader as it expects CLI.

        # Setup folders
        folders = dd.setupFolders(is_colab=dd.detectColab(), PROJECT_DIR=PROJECT_DIR, pargs=pargs)

        # Report System Details
        dd.systemDetails(pargs)

        # Get CUDA Device
        device = dd.getDevice(pargs)

        dd.start_run(pargs=pargs, folders=folders, device=device, is_colab=dd.detectColab())


button.on_click(run_dd)
