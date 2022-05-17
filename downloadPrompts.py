import wget, os
from loguru import logger
from pydotted import pydot
import hashlib


def loadModels(folders=pydot({"prompt_salad_path": "prompts"})):
    """Downloads prompts required for promptSalad function in use Disco Diffusion

    Args:
        folders (JSON): Folder parameters (e.g. `{"prompt_salad_path":"path/to/download/prompts"}`)
    """
    # Download models if not present
    for m in [
        {
            "file": f"{folders.prompt_salad_path}/adjectives.txt",
            "sources": [
                {"url": "https://raw.githubusercontent.com/entmike/prompt_gen/main/adjectives.txt"},
            ],
        },
        {
            "file": f"{folders.prompt_salad_path}/animals.txt",
            "sources": [
                {"url": "https://raw.githubusercontent.com/entmike/prompt_gen/main/animals.txt"},
            ],
        },
        {
            "file": f"{folders.prompt_salad_path}/artists.txt",
            "sources": [
                {"url": "https://raw.githubusercontent.com/entmike/prompt_gen/main/artists.txt"},
            ],
        },
        {
            "file": f"{folders.prompt_salad_path}/colors.txt",
            "sources": [
                {"url": "https://raw.githubusercontent.com/entmike/prompt_gen/main/colors.txt"},
            ],
        },
        {
            "file": f"{folders.prompt_salad_path}/locations.txt",
            "sources": [
                {"url": "https://raw.githubusercontent.com/entmike/prompt_gen/main/locations.txt"},
            ],
        },
        {
            "file": f"{folders.prompt_salad_path}/of_something.txt",
            "sources": [
                {"url": "https://raw.githubusercontent.com/entmike/prompt_gen/main/of_something.txt"},
            ],
        },
        {
            "file": f"{folders.prompt_salad_path}/shapes.txt",
            "sources": [
                {"url": "https://raw.githubusercontent.com/entmike/prompt_gen/main/shapes.txt"},
            ],
        },
        {
            "file": f"{folders.prompt_salad_path}/styles.txt",
            "sources": [
                {"url": "https://raw.githubusercontent.com/entmike/prompt_gen/main/styles.txt"},
            ],
        },
        {
            "file": f"{folders.prompt_salad_path}/templates.py",
            "sources": [
                {"url": "https://raw.githubusercontent.com/entmike/prompt_gen/main/templates.py"},
            ],
        },
        {
            "file": f"{folders.prompt_salad_path}/things.txt",
            "sources": [
                {"url": "https://raw.githubusercontent.com/entmike/prompt_gen/main/things.txt"},
            ],
        },
    ]:
        if not os.path.exists(f'{m["file"]}'):
            downloaded = False
            for source in m["sources"]:
                if not downloaded:
                    url = source["url"]
                    try:
                        logger.info(f'🌍 (First time setup): Downloading model from {url} to {m["file"]}')
                        wget.download(url, m["file"])
                        downloaded = True
                    except:
                        logger.error(f"Download failed.  Fallback URLs will be attempted until exhausted.")
            if downloaded == False:
                logger.error(f"🛑 Could NOT download {m['file']} from any sources! 🛑")
        else:
            logger.success(f'✅ Model already downloaded: {m["file"]}')


def main():
    loadModels(pydot({"prompt_salad_path": "prompts"}))


if __name__ == "__main__":
    main()
