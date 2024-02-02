from pydantic import BaseModel
from typing import Optional

# 데이터타입(스키마) 정의


class ModelInput(BaseModel):
    prompt: str


class ModelOutput(BaseModel):
    image: str  # base64-encoded image data (오류 발생할 경우 수정 필요)
