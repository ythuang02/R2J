# **R**ewrite **to** **J**ailbreak (R2J)

This is the official repository for the paper [[ACL2025 Findings] Rewrite to Jailbreak: Discover Learnable and Transferable Implicit Harmfulness Instruction](https://arxiv.org/abs/2502.11084)

![](repo.png)
---

## 0. Prepare the code & env

We recommend using Conda to create a virtual environment.
```bash
conda create -n R2J python==3.11
conda activate R2J

git clone https://github.com/ythuang02/R2J
```

> [!NOTE]
> 
> Git cannot clone this anonymous repository, please download it from the webpage manually. 

We conduct Supervised Fine-Tuning (SFT) based on the open-source project [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory/tree/1c910079d8544c433add2d949a8378822d1425c9).

```bash
cd R2J
git submodule init
git submodule update
```

**Installation of LLaMA-Factory**

```bash
cd factory
pip install -e ".[torch,deepspeed,bitsandbytes]"
```

## 1. Setting up the configs

Please refer to [configs/README.md](configs/README.md) for checking the details about the format of configuration files.

We also provide examples of three experiments, which are:

- Direct jailbreak attack at [configs/train.yaml](configs/train.yaml)
- Transfer attack across model at [configs/transfer_attack_model.yaml](configs/transfer_attack_model.yaml)
- Transfer attack across dataset at [configs/transfer_attack_dataset.yaml](configs/transfer_attack_dataset.yaml)

> [!Note]
>
> At least need to modify the `model_path`, `base_url`, `key` and `gpu` in the configuration file.

## 2. Run the experiment

```bash
python main.py configs/<your config file>
```

## Encountered issuess?

We also provide the conda environment file as follows:

<details>
<summary>Conda Environment</summary>

```
name: R2J
dependencies:
  - _libgcc_mutex=0.1=main
  - _openmp_mutex=5.1=1_gnu
  - bzip2=1.0.8=h5eee18b_6
  - ca-certificates=2024.3.11=h06a4308_0
  - ld_impl_linux-64=2.38=h1181459_1
  - libffi=3.4.4=h6a678d5_1
  - libgcc-ng=11.2.0=h1234567_1
  - libgomp=11.2.0=h1234567_1
  - libstdcxx-ng=11.2.0=h1234567_1
  - libuuid=1.41.5=h5eee18b_0
  - ncurses=6.4=h6a678d5_0
  - openssl=1.1.1w=h7f8727e_0
  - pip=24.0=py311h06a4308_0
  - python=3.11.0=h7a1cb2a_3
  - readline=8.2=h5eee18b_0
  - setuptools=69.5.1=py311h06a4308_0
  - sqlite=3.45.3=h5eee18b_0
  - tk=8.6.14=h39e8969_0
  - wheel=0.43.0=py311h06a4308_0
  - xz=5.4.6=h5eee18b_1
  - zlib=1.2.13=h5eee18b_1
  - pip:
      - accelerate==0.31.0
      - aiofiles==23.2.1
      - aiohttp==3.9.5
      - aiosignal==1.3.1
      - altair==5.3.0
      - annotated-types==0.7.0
      - anyio==4.4.0
      - attrs==23.2.0
      - bitsandbytes==0.43.1
      - certifi==2024.6.2
      - charset-normalizer==3.3.2
      - click==8.1.7
      - contourpy==1.2.1
      - cycler==0.12.1
      - datasets==2.19.2
      - deepspeed==0.14.0
      - dill==0.3.8
      - dnspython==2.6.1
      - docstring-parser==0.16
      - einops==0.8.0
      - email-validator==2.1.1
      - fastapi==0.111.0
      - fastapi-cli==0.0.4
      - ffmpy==0.3.2
      - filelock==3.14.0
      - fire==0.6.0
      - fonttools==4.53.0
      - frozenlist==1.4.1
      - fsspec==2024.3.1
      - gradio==4.36.1
      - gradio-client==1.0.1
      - h11==0.14.0
      - hjson==3.1.0
      - httpcore==1.0.5
      - httptools==0.6.1
      - httpx==0.27.0
      - huggingface-hub==0.23.3
      - idna==3.7
      - importlib-resources==6.4.0
      - jinja2==3.1.4
      - jsonschema==4.22.0
      - jsonschema-specifications==2023.12.1
      - kiwisolver==1.4.5
      - llmtuner==0.7.1
      - markdown-it-py==3.0.0
      - markupsafe==2.1.5
      - matplotlib==3.9.0
      - mdurl==0.1.2
      - mpmath==1.3.0
      - multidict==6.0.5
      - multiprocess==0.70.16
      - networkx==3.3
      - ninja==1.11.1.1
      - numpy==1.26.4
      - nvidia-cublas-cu12==12.1.3.1
      - nvidia-cuda-cupti-cu12==12.1.105
      - nvidia-cuda-nvrtc-cu12==12.1.105
      - nvidia-cuda-runtime-cu12==12.1.105
      - nvidia-cudnn-cu12==8.9.2.26
      - nvidia-cufft-cu12==11.0.2.54
      - nvidia-curand-cu12==10.3.2.106
      - nvidia-cusolver-cu12==11.4.5.107
      - nvidia-cusparse-cu12==12.1.0.106
      - nvidia-nccl-cu12==2.20.5
      - nvidia-nvjitlink-cu12==12.5.40
      - nvidia-nvtx-cu12==12.1.105
      - orjson==3.10.4
      - packaging==24.1
      - pandas==2.2.2
      - peft==0.11.1
      - pillow==10.3.0
      - protobuf==5.27.1
      - psutil==5.9.8
      - py-cpuinfo==9.0.0
      - pyarrow==16.1.0
      - pyarrow-hotfix==0.6
      - pydantic==2.7.3
      - pydantic-core==2.18.4
      - pydub==0.25.1
      - pygments==2.18.0
      - pynvml==11.5.0
      - pyparsing==3.1.2
      - python-dateutil==2.9.0.post0
      - python-dotenv==1.0.1
      - python-multipart==0.0.9
      - pytz==2024.1
      - pyyaml==6.0.1
      - referencing==0.35.1
      - regex==2024.5.15
      - requests==2.32.3
      - rich==13.7.1
      - rpds-py==0.18.1
      - ruff==0.4.8
      - safetensors==0.4.3
      - scipy==1.13.1
      - semantic-version==2.10.0
      - sentencepiece==0.2.0
      - shellingham==1.5.4
      - shtab==1.7.1
      - six==1.16.0
      - sniffio==1.3.1
      - sse-starlette==2.1.0
      - starlette==0.37.2
      - sympy==1.12.1
      - termcolor==2.4.0
      - tokenizers==0.19.1
      - tomlkit==0.12.0
      - toolz==0.12.1
      - torch==2.3.1
      - tqdm==4.66.4
      - transformers==4.41.2
      - triton==2.3.1
      - trl==0.9.4
      - typer==0.12.3
      - typing-extensions==4.12.2
      - tyro==0.8.4
      - tzdata==2024.1
      - ujson==5.10.0
      - urllib3==2.2.1
      - uvicorn==0.30.1
      - uvloop==0.19.0
      - watchfiles==0.22.0
      - websockets==11.0.3
      - xxhash==3.4.1
      - yarl==1.9.4
```
</details>

## Citation

```
@article{huang2025rewrite,
  title={Rewrite to Jailbreak: Discover Learnable and Transferable Implicit Harmfulness Instruction},
  author={Huang, Yuting and Liu, Chengyuan and Feng, Yifeng and Wu, Chao and Wu, Fei and Kuang, Kun},
  journal={arXiv preprint arXiv:2502.11084},
  year={2025}
}
```