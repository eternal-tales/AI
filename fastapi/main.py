from fastapi import Depends, FastAPI, HTTPException

import generate
import schema

app = FastAPI()

# ---------------------------------------------------------------------------

# Dependency

# USER_NOT_FOUND = HTTPException(
#    status_code=400, detail="User not found.")  # FAIL

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
# 4) 생성한 이미지를 S3에 저장 / 일단 저장장


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.create_user(db=db, user=user)
    return db_user

# 전체 조회


@app.get("/users", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

# 특정 조회


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise USER_NOT_FOUND
    return db_user

# 특정 수정 (id 는 수정 불가)


@app.put("/users/{user_id}", response_model=schemas.CompleteResponse)
def update_user(user_id: int, user_data: schemas.UserUpdate, db: Session = Depends(get_db)):  # 수정 필요
    # 체크
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise USER_NOT_FOUND
    action = crud.update_user(
        db=db, user_id=user_id, name=user_data.name, age=user_data.age, role=user_data.role)
    return action

# 특정 삭제


@app.delete("/users/{user_id}", response_model=schemas.CompleteResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # 체크
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise USER_NOT_FOUND
    action = crud.delete_user(db=db, user_id=user_id)
    return action
