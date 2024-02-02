from pydantic import BaseModel
from fastapi.models import UploadFile
from typing import Optional

# 데이터타입(스키마) 정의

# Agent Modelling - 이미지 5장


class AgentInput(BaseModel):
    img1: Optional[UploadFile] = None
    img2: Optional[UploadFile] = None
    img3: Optional[UploadFile] = None
    img4: Optional[UploadFile] = None
    img5: Optional[UploadFile] = None


# Agent Modelling - 학습된 모델 체크포인트
class AgentOutput(BaseModel):
    ckpt: str  # 파일경로


# Chatting - 채팅 트리거 메세지
class ChatInput(BaseModel):
    msg: str  # 사용자의 트리거 메세지 문장


# Chatting - 채팅 메세지에 따라 생성된 이미지 1장
class ChatOutput(BaseModel):
    img: str  # base64-encoded image data (오류 발생할 경우 수정 필요)
