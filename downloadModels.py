import wget, os
from loguru import logger
from pydotted import pydot


def loadModels(folders=pydot({"model_path": "models"})):
    """Downloads models required to use Disco Diffusion

    Args:
        folders (JSON): Folder parameters (e.g. `{"model_path":"path/to/download/models"}`)
    """
    # Download models if not present
    for m in [
        {
            "file": f"{folders.model_path}/dpt_large-midas-2f21e586.pt",
            "sources": [
                {"url": "https://github.com/intel-isl/DPT/releases/download/1_0/dpt_large-midas-2f21e586.pt"},
                {"url": "https://ipfs.io/ipfs/QmbpkBqVrayBzaxHMSnk917ng2EopZsdFK8pFkku9sbr8H?filename=dpt_large-midas-2f21e586.pt"},
            ],
        },
        {
            "file": f"{folders.model_path}/512x512_diffusion_uncond_finetune_008100.pt",
            "sources": [
                {"url": "https://v-diffusion.s3.us-west-2.amazonaws.com/512x512_diffusion_uncond_finetune_008100.pt"},
                {"url": "https://huggingface.co/lowlevelware/512x512_diffusion_unconditional_ImageNet/resolve/main/512x512_diffusion_uncond_finetune_008100.pt"},
                {"url": "https://ipfs.io/ipfs/QmYNhbgnjPRuprob6WiELb3egd8rZa2xTEYGzAfkLuaKJw?filename=512x512_diffusion_uncond_finetune_008100.pt"},
            ],
        },
        {
            "file": f"{folders.model_path}/256x256_diffusion_uncond.pt",
            "sources": [
                {"url": "https://openaipublic.blob.core.windows.net/diffusion/jul-2021/256x256_diffusion_uncond.pt"},
                {"url": "https://www.dropbox.com/s/9tqnqo930mpnpcn/256x256_diffusion_uncond.pt"},
                {"url": "https://ipfs.io/ipfs/QmRkZ4JBLHwpZqeAuULYeGzo3TZqfgnrg6bFvUXFneotP9?filename=256x256_diffusion_uncond.pt"},
            ],
        },
        {
            "file": f"{folders.model_path}/secondary_model_imagenet_2.pth",
            "sources": [
                {"url": "https://v-diffusion.s3.us-west-2.amazonaws.com/secondary_model_imagenet_2.pth"},
                {"url": "https://ipfs.io/ipfs/QmX1VDNBAsAbupaLLkL2AxTQsxbFFYac8rqM9croNm3H9U?filename=secondary_model_imagenet_2.pth"},
            ],
        },
        {
            "file": f"{folders.model_path}/AdaBins_nyu.pt",
            "sources": [
                {"url": "https://cloudflare-ipfs.com/ipfs/Qmd2mMnDLWePKmgfS8m6ntAg4nhV5VkUyAydYBp8cWWeB7/AdaBins_nyu.pt"},
                {"url": "https://ipfs.io/ipfs/QmfZv38n2u3b3gZMtTqSwEXDEM27BtQdksefCYy7HA9VAv?filename=AdaBins_nyu.pt"},
            ],
        },
        {
            "file": f"{folders.model_path}/RN50.pt",
            "sources": [{"url": "https://openaipublic.azureedge.net/clip/models/afeb0e10f9e5a86da6080e35cf09123aca3b358a0c3e3b6c78a7b63bc04b6762/RN50.pt"}],
        },
        {
            "file": f"{folders.model_path}/RN101.pt",
            "sources": [{"url": "https://openaipublic.azureedge.net/clip/models/8fa8567bab74a42d41c5915025a8e4538c3bdbe8804a470a72f30b0d94fab599/RN101.pt"}],
        },
        {
            "file": f"{folders.model_path}/RN50x4.pt",
            "sources": [{"url": "https://openaipublic.azureedge.net/clip/models/7e526bd135e493cef0776de27d5f42653e6b4c8bf9e0f653bb11773263205fdd/RN50x4.pt"}],
        },
        {
            "file": f"{folders.model_path}/RN50x16.pt",
            "sources": [{"url": "https://openaipublic.azureedge.net/clip/models/52378b407f34354e150460fe41077663dd5b39c54cd0bfd2b27167a4a06ec9aa/RN50x16.pt"}],
        },
        {
            "file": f"{folders.model_path}/RN50x64.pt",
            "sources": [{"url": "https://openaipublic.azureedge.net/clip/models/be1cfb55d75a9666199fb2206c106743da0f6468c9d327f3e0d0a543a9919d9c/RN50x64.pt"}],
        },
        {
            "file": f"{folders.model_path}/ViT-B-32.pt",
            "sources": [{"url": "https://openaipublic.azureedge.net/clip/models/40d365715913c9da98579312b702a82c18be219cc2a73407c4526f58eba950af/ViT-B-32.pt"}],
        },
        {
            "file": f"{folders.model_path}/ViT-B-16.pt",
            "sources": [{"url": "https://openaipublic.azureedge.net/clip/models/5806e77cd80f8b59890b7e101eabd078d9fb84e6937f9e85e4ecb61988df416f/ViT-B-16.pt"}],
        },
        {
            "file": f"{folders.model_path}/ViT-L-14.pt",
            "sources": [{"url": "https://openaipublic.azureedge.net/clip/models/b8cca3fd41ae0c99ba7e8951adf17d267cdb84cd88be6f7c2e0eca1737a03836/ViT-L-14.pt"}],
        },
        {
            "file": f"{folders.model_path}/ViT-L-14-336px.pt",
            "sources": [{"url": "https://openaipublic.azureedge.net/clip/models/3035c92b350959924f9f00213499208652fc7ea050643e8b385c2dac08641f02/ViT-L-14-336px.pt"}],
        },
        {"file": f"{folders.model_path}/vgg16-397923af.pth", "sources": [{"url": "https://download.pytorch.org/models/vgg16-397923af.pth"}]},
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
        else:
            logger.success(f'✅ Model already downloaded: {m["file"]}')


def main():
    loadModels(pydot({"model_path": "models"}))


if __name__ == "__main__":
    main()
