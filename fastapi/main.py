from fastapi import FastAPI, HTTPException
from typing import List

import torch
import diffusers
from PIL import Image
from torch import autocast
from diffusers import StableDiffusionPipeline

from inference import generate

# ---------------------------------------------------------------------------

app = FastAPI()

# ---------------------------------------------------------------------------

# 이미지 생성 후 리턴


@app.get("/generate-image")  # response model 생략 (바로 S3 저장)
async def generate_image(prompt: str):  # prompt 는 사용자에게 input 으로 받아야 한다.
    output_image = generate(prompt)
    # 생성파트까지만 작성, S3 전송 파트는 별도로 구현
