import wget, os
from loguru import logger
from pydotted import pydot
import hashlib
import ipywidgets as widgets
from IPython import display


def loadModels(folders=pydot({"model_path": "models"})):
    """Downloads models required to use Disco Diffusion

    Args:
        folders (JSON): Folder parameters (e.g. `{"model_path":"path/to/download/models"}`)
    """
    # Download models if not present

    models_config = [
        {
            "file": f"{folders.model_path}/dpt_large-midas-2f21e586.pt",
            "hash": "2f21e586477d90cb9624c7eef5df7891edca49a1c4795ee2cb631fd4daa6ca69",
            "sources": [
                {"url": "https://github.com/intel-isl/DPT/releases/download/1_0/dpt_large-midas-2f21e586.pt"},
                {"url": "https://ipfs.io/ipfs/QmbpkBqVrayBzaxHMSnk917ng2EopZsdFK8pFkku9sbr8H?filename=dpt_large-midas-2f21e586.pt"},
            ],
        },
        {
            "file": f"{folders.model_path}/512x512_diffusion_uncond_finetune_008100.pt",
            "hash": "9c111ab89e214862b76e1fa6a1b3f1d329b1a88281885943d2cdbe357ad57648",
            "sources": [
                {"url": "https://v-diffusion.s3.us-west-2.amazonaws.com/512x512_diffusion_uncond_finetune_008100.pt"},
                {"url": "https://huggingface.co/lowlevelware/512x512_diffusion_unconditional_ImageNet/resolve/main/512x512_diffusion_uncond_finetune_008100.pt"},
                {"url": "https://ipfs.io/ipfs/QmYNhbgnjPRuprob6WiELb3egd8rZa2xTEYGzAfkLuaKJw?filename=512x512_diffusion_uncond_finetune_008100.pt"},
            ],
        },
        {
            "file": f"{folders.model_path}/256x256_diffusion_uncond.pt",
            "hash": "a37c32fffd316cd494cf3f35b339936debdc1576dad13fe57c42399a5dbc78b1",
            "sources": [
                {"url": "https://openaipublic.blob.core.windows.net/diffusion/jul-2021/256x256_diffusion_uncond.pt"},
                {"url": "https://www.dropbox.com/s/9tqnqo930mpnpcn/256x256_diffusion_uncond.pt"},
                {"url": "https://ipfs.io/ipfs/QmRkZ4JBLHwpZqeAuULYeGzo3TZqfgnrg6bFvUXFneotP9?filename=256x256_diffusion_uncond.pt"},
            ],
        },
        {
            "file": f"{folders.model_path}/secondary_model_imagenet_2.pth",
            "hash": "983e3de6f95c88c81b2ca7ebb2c217933be1973b1ff058776b970f901584613a",
            "sources": [
                {"url": "https://v-diffusion.s3.us-west-2.amazonaws.com/secondary_model_imagenet_2.pth"},
                {"url": "https://the-eye.eu/public/AI/models/v-diffusion/secondary_model_imagenet_2.pth"},
                {"url": "https://ipfs.io/ipfs/QmX1VDNBAsAbupaLLkL2AxTQsxbFFYac8rqM9croNm3H9U?filename=secondary_model_imagenet_2.pth"},
            ],
        },
        {
            "file": f"{folders.model_path}/AdaBins_nyu.pt",
            "hash": "3c917d1b86d058918d4055e70b2cdb9696ec4967bb2d8f05c0051263c1ac9641",
            "sources": [
                {"url": "https://cloudflare-ipfs.com/ipfs/Qmd2mMnDLWePKmgfS8m6ntAg4nhV5VkUyAydYBp8cWWeB7/AdaBins_nyu.pt"},
                {"url": "https://ipfs.io/ipfs/QmfZv38n2u3b3gZMtTqSwEXDEM27BtQdksefCYy7HA9VAv?filename=AdaBins_nyu.pt"},
            ],
        },
        {
            "file": f"{folders.model_path}/RN50.pt",
            "hash": "afeb0e10f9e5a86da6080e35cf09123aca3b358a0c3e3b6c78a7b63bc04b6762",
            "sources": [{"url": "https://openaipublic.azureedge.net/clip/models/afeb0e10f9e5a86da6080e35cf09123aca3b358a0c3e3b6c78a7b63bc04b6762/RN50.pt"}],
        },
        {
            "file": f"{folders.model_path}/RN101.pt",
            "hash": "8fa8567bab74a42d41c5915025a8e4538c3bdbe8804a470a72f30b0d94fab599",
            "sources": [{"url": "https://openaipublic.azureedge.net/clip/models/8fa8567bab74a42d41c5915025a8e4538c3bdbe8804a470a72f30b0d94fab599/RN101.pt"}],
        },
        {
            "file": f"{folders.model_path}/RN50x4.pt",
            "hash": "7e526bd135e493cef0776de27d5f42653e6b4c8bf9e0f653bb11773263205fdd",
            "sources": [{"url": "https://openaipublic.azureedge.net/clip/models/7e526bd135e493cef0776de27d5f42653e6b4c8bf9e0f653bb11773263205fdd/RN50x4.pt"}],
        },
        {
            "file": f"{folders.model_path}/RN50x16.pt",
            "hash": "52378b407f34354e150460fe41077663dd5b39c54cd0bfd2b27167a4a06ec9aa",
            "sources": [{"url": "https://openaipublic.azureedge.net/clip/models/52378b407f34354e150460fe41077663dd5b39c54cd0bfd2b27167a4a06ec9aa/RN50x16.pt"}],
        },
        {
            "file": f"{folders.model_path}/RN50x64.pt",
            "hash": "be1cfb55d75a9666199fb2206c106743da0f6468c9d327f3e0d0a543a9919d9c",
            "sources": [{"url": "https://openaipublic.azureedge.net/clip/models/be1cfb55d75a9666199fb2206c106743da0f6468c9d327f3e0d0a543a9919d9c/RN50x64.pt"}],
        },
        {
            "file": f"{folders.model_path}/ViT-B-32.pt",
            "hash": "40d365715913c9da98579312b702a82c18be219cc2a73407c4526f58eba950af",
            "sources": [{"url": "https://openaipublic.azureedge.net/clip/models/40d365715913c9da98579312b702a82c18be219cc2a73407c4526f58eba950af/ViT-B-32.pt"}],
        },
        {
            "file": f"{folders.model_path}/ViT-B-16.pt",
            "hash": "5806e77cd80f8b59890b7e101eabd078d9fb84e6937f9e85e4ecb61988df416f",
            "sources": [{"url": "https://openaipublic.azureedge.net/clip/models/5806e77cd80f8b59890b7e101eabd078d9fb84e6937f9e85e4ecb61988df416f/ViT-B-16.pt"}],
        },
        {
            "file": f"{folders.model_path}/ViT-L-14.pt",
            "hash": "b8cca3fd41ae0c99ba7e8951adf17d267cdb84cd88be6f7c2e0eca1737a03836",
            "sources": [{"url": "https://openaipublic.azureedge.net/clip/models/b8cca3fd41ae0c99ba7e8951adf17d267cdb84cd88be6f7c2e0eca1737a03836/ViT-L-14.pt"}],
        },
        {
            "file": f"{folders.model_path}/ViT-L-14-336px.pt",
            "hash": "3035c92b350959924f9f00213499208652fc7ea050643e8b385c2dac08641f02",
            "sources": [{"url": "https://openaipublic.azureedge.net/clip/models/3035c92b350959924f9f00213499208652fc7ea050643e8b385c2dac08641f02/ViT-L-14-336px.pt"}],
        },
        {
            "file": f"{folders.model_path}/vgg16-397923af.pth",
            "hash": "397923af8e79cdbb6a7127f12361acd7a2f83e06b05044ddf496e83de57a5bf0",
            "sources": [{"url": "https://download.pytorch.org/models/vgg16-397923af.pth"}],
        },
        {
            "file": f"{folders.model_path}/256x256_openai_comics_faces_by_alex_spirin_084000.pt",
            "hash": "f587fd6d2edb093701931e5083a13ab6b76b3f457b60efd1aa873d60ee3d6388",
            "sources": [{"url": "https://github.com/Sxela/DiscoDiffusion-Warp/releases/download/v0.1.0/256x256_openai_comics_faces_by_alex_spirin_084000.pt"}],
        },
        {
            "file": f"{folders.model_path}/pixel_art_diffusion_hard_256.pt",
            "hash": "be4a9de943ec06eef32c65a1008c60ad017723a4d35dc13169c66bb322234161",
            "sources": [{"url": "https://huggingface.co/KaliYuga/pixel_art_diffusion_hard_256/resolve/main/pixel_art_diffusion_hard_256.pt"}],
        },
        {
            "file": f"{folders.model_path}/pixel_art_diffusion_soft_256.pt",
            "hash": "d321590e46b679bf6def1f1914b47c89e762c76f19ab3e3392c8ca07c791039c",
            "sources": [{"url": "https://huggingface.co/KaliYuga/pixel_art_diffusion_soft_256/resolve/main/pixel_art_diffusion_soft_256.pt"}],
        },
        {
            "file": f"{folders.model_path}/lsun_uncond_100M_1200K_bs128.pt",
            "hash": "38e66420ba5c703df8ce78750721976e13442064b5df847b82f05ebc65120534",
            "sources": [{"url": "https://openaipublic.blob.core.windows.net/diffusion/march-2021/lsun_uncond_100M_1200K_bs128.pt"}],
        },
        {
            "file": f"{folders.model_path}/vit_b_16_plus_240-laion400m_e31-8fb26589.pt",
            "hash": "8fb26589b9a8bab2e7a683d280e48df89b8e742f3a82132707282620b36facba",
            "sources": [{"url": "https://github.com/mlfoundations/open_clip/releases/download/v0.2-weights/vit_b_16_plus_240-laion400m_e31-8fb26589.pt"}],
        },
    ]

    modelProgress = widgets.IntProgress(
        value=0, min=0, max=len(models_config), bar_style="info", orientation="horizontal", description="Downloading"  # 'success', 'info', 'warning', 'danger' or ''
    )

    print("Making sure required models are downloaded")
    try:
        display(modelProgress)
    except:
        logger.info("Downloading...")

    ## TODO: Make this show incremental progress
    ## TODO: Make this download in parallel

    for m in models_config:
        if not os.path.exists(f'{m["file"]}'):
            downloaded = False
            for source in m["sources"]:
                if not downloaded:
                    url = source["url"]
                    try:
                        logger.info(f'🌍 (First time setup): Downloading model from {url} to {m["file"]}')
                        wget.download(url, m["file"])
                        print("")
                        with open(m["file"], "rb") as f:
                            bytes = f.read()  # read entire file as bytes
                            readable_hash = hashlib.sha256(bytes).hexdigest()
                            if readable_hash == m["hash"]:
                                logger.success(f"✅ SHA-256 hash matches: {readable_hash}")
                                modelProgress.value = modelProgress.value + 1
                                downloaded = True
                            else:
                                logger.error(f"🛑 Wrong hash! '{readable_hash}' instead of '{m['hash']}'")
                                os.remove(m["file"])
                                raise Exception("Bad hash")
                    except:
                        logger.error(f"Download failed.  Fallback URLs will be attempted until exhausted.")
            if downloaded == False:
                logger.error(f"🛑 Could NOT download {m['file']} from any sources! 🛑")
        else:
            modelProgress.value = modelProgress.value + 1
            logger.success(f'✅ Model already downloaded: {m["file"]}')


def main():
    loadModels(pydot({"model_path": "models"}))


if __name__ == "__main__":
    main()
