# Disco Diffusion

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) <a href="https://colab.research.google.com/github/entmike/disco-diffusion-1/blob/main/Simplified_Disco_Diffusion.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab"/></a>

A frankensteinian amalgamation of notebooks, models and techniques for the generation of AI Art and Animations.

<img src="images_out/TimeToDisco/TimeToDisco(0)_0.png" />

## Changes in this Fork

- Focus on running from Windows, Linux, Google Colab, and Docker via either CLI or Notebook.
- Move all functions possible out of the main `disco.py` module into `dd.py` so that `disco.py` can become readable.
- Instead changing parameters directly in `disco.py`, parameters can be controlled by environment variables, command-line arguments, or config (YAML) files.
- Allows YAML parameter files to be used as inputs. (See `examples/configs` for more)
- SQLite support to store parameters and images for querying against later.
- Iterate over parameters via `modifiers` and `multipliers`. (See `examples/configs` for more)

## Windows First-time Setup (Anaconda)

Follow these steps for the first time that you are running Disco Diffusion from Windows.

### Pre-requisites

- Anaconda installed
- Nvidia CUDA Toolkit Installed
- MS VS Community Installed with C++ checkmarked

1. From **Anaconda Powershell Prompt**:
    
    This command will allow you to use `conda` from a "regular" powershell session.
    ```
    conda init powershell
    exit
    ```

2. From your **VS Code Powershell prompt**:

    **Note:** These commands should be run from the working directory of this cloned repository.

    This command will pull all dependencies needed by Disco Diffusion into a conda environment called `discodiffusion`
    ```
    conda env create -f environment.yml
    conda activate discodiffusion
    ```

      - **Note:** If you have already activated a `discodiffusion` conda environment, you can refresh it if this repo has changed by typing:

        `conda env update --prefix discodiffusion --file environment.yml  --prune`

3. Compile `pytorch3d`
    
    **Note:** These commands should be run from the working directory of this cloned repository.
    
    For reason I'm not 100% clear on, `pytorch3d` must be compiled in Windows.  (Hence the requirement for C++ tool mentioned in Pre-requisties...)
    ```
    git clone https://github.com/facebookresearch/pytorch3d.git
    cd pytorch3d
    python setup.py install
    cd ..
    ```
4. Execute a test run:

    The following test run will run with all defaults (so "the lighthouse run" as it is coined.)  Image output and current image progress (`progress.png`) will be stored in `images_out`.
    ```
    conda activate discodiffusion
    python disco.py
    ```

## First-time Setup (`pip`)
   
   - Windows PowerShell:
     ```powershell
     python3 -m pip install --user virtualenv
     python -m venv .\.venv\discodiffusion
     .venv\discodiffusion\Scripts\Activate.ps1
     pip install -r requirements.txt
     ```

   - Windows Command Prompt:
     ```cmd
     python3 -m pip install --user virtualenv
     python -m venv .\.venv\discodiffusion
     .venv\discodiffusion\Scripts\Activate.cmd
     pip install -r requirements.txt
     ```
   - Linux

     ```bash
     python3 -m pip install --user virtualenv
     python -m venv ./.venv/discodiffusion
     pip install -r requirements.txt
     ```
   
   - Test Run

     ```powershell
     python disco.py
     ```

     A batch run should begin.  Kill with **Control+C** Example:
        ```
        Using device: cuda:0
        💻 Starting Run: TimeToDisco(0) at frame 0
        🌱 Randomly using seed: 1825817222
        Prepping models...
        🤖 Loading model 'ViT-B/32'...
        🤖 Loading model 'ViT-B/16'...
        🤖 Loading model 'RN50'...
        🤖 Loading secondary model...
        🤖 Loading LPIPS...
        🌱 Seed used: 1825817222
        Frame 0 📝 Prompt: ['A beautiful painting of a singular lighthouse, shining its light across a tumultuous sea of blood by greg rutkowski and thomas kinkade, Trending on artstation.', 'yellow color scheme']
        Batches:   0%|          | 0/50 [00:00<?, ?it/s]

        4%|████▌                                                                                                         | 10/240 [00:14<05:05,  1.33s/it]
        ```
