from fastapi.models import FastAPI, File, UploadFile, HTTPException
from typing import List
import base64
import aiofiles
import os

from schema import AgentInput, AgentOutput, ChatInput, ChatOutput
import models.config
import models.dreambooth
import models.generate
import models.preprocess
import models.stablediffusion
import models.train

app = FastAPI()

# ---------------------------------------------------------------------------

# Dependency (우선 생략)

# -----------------------------------------------------------------------------

# PART 1. Pet Agent Modelling
# 1-1. 이미지 받아오기 (생략)

# 1-2. 받은 이미지 5장으로 모델 '학습' 및 '저장' (체크포인트는 별도로 return 하지 않고, 바로 저장 가능)
@app.post("/train-model", response_model=AgentOutput)
async def train_model(files: List[UploadFile] = File(...)):
    if len(files) != 5:
        raise HTTPException(
            status_code=400, detail="반드시 5장을 업로드해주세요.")

    # 임시 저장 공간
    saved_files = []
    try:
        for file in files:
            async with aiofiles.open(f'tmp/{file.filename}', 'wb') as out_file:
                content = await file.read()
                await out_file.write(content)
            saved_files.append(f'tmp/{file.filename}')

        # (1) Config
        models.config.install_dependencies()

        # (2) Model Download - 작성 필요 (각 모듈 함수로 감싸줘야 한다.)

        # (3) DreamBooth - 작성 필요

        # (4) Preprocess - 작성 필요

        # (5) Train - 작성 필요

        # 모델 체크포인트 경로 - 작성 필요
        ckpt_path = train_module.train(saved_files)
        
        # 학습한 후, 사용된 소스 이미지들 삭제
        for file_path in saved_files:
            os.remove(file_path)
        return AgentOutput(ckpt=ckpt_path)

    except Exception as e:
        # 오류 발생
        for file_path in saved_files:
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------------------------------------------

# PART 2. Image Generating
# 2-1. 모델 로드 및 학습된 쳌포 플러그인
@app.get("/load-model")
async def load_model(ckpt: str):
    model = # 작성 필요
    # 별도의 return 값 없음

# 2-2. 이미지 생성 후 전송
# 트리거 시나리오 선택 > 해당 프롬프트 넣어 생성
@app.post("/generate-image", response_model=ChatOutput)
async def generate_image(msg: str):
    output_image = # 작성 필요 (msg))
    
    # 생성파트까지만 작성, S3 전송 파트는 별도로 구현
    
    
        
# -----------------------------------------------------------------------------


# ENDPOINTS
# 기능에 따른 순서는 결국

# Agent Modelling
# 1) 이미지 사진 GET, 5장 / ( 어디로부터 GET ) 신경 X 임의로
# 2) 모델에서 (GPU 연결하여) 모델 학습
# 3) 학습 완료된 체크포인트 저장 / 디렉토리 안에 저장
# 4) 해당 체크포인트가 플러그인 상태로 모델 '유지'


# Chatting
# 1) 사용자의 발화 GET / GET  신경 X
# 2) 랜덤한 상황의 프롬프트가 미리 필요, 해당 프롬프트와 가장 유사한(알고리즘 따라) 프롬프트 GET
# 3) (모델 유지에 대해서) 해당 프롬프트에 대한 이미지 생성
# 4) 생성한 이미지를 S3에 저장 / 일단 저장