from fastapi import FastAPI, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from typing import List
import pandas as pd
import numpy as np
import faiss
import torch
from sentence_transformers import SentenceTransformer, util
from pydantic import BaseModel

app = FastAPI()

class Request(BaseModel):
    policy_id: int
    question: str

# SentenceTransformer 모델 초기화
model = SentenceTransformer("Huffon/sentence-klue-roberta-base")

@app.get("/")
async def root():
    return {"message": "Hello World"}

# AI 모델1 엔드포인트
@app.post("/top3")
async def top3(request: Request):
    try:
        data = request.json()
        domain = request.policy_id
        user_question = request.question

        # 데이터 불러오기 및 임베딩 벡터 초기화
        df = pd.read_excel(f"./GW_FAQ.xlsx", sheet_name=domain - 1)
        embeddings = np.load(f"./FAQ_embedding/embeddings_{domain}.npy")
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)

        # 사용자 질문에 대한 임베딩 벡터 생성
        query_embedding = model.encode(user_question, normalize_embeddings=True)

        # 유사한 질문 3개 찾기
        top_k = 3
        distances, indices = index.search(np.expand_dims(query_embedding, axis=0), top_k)

        # 결과 반환
        similar_questions = df.iloc[indices[0]]['Q'].tolist()
        return JSONResponse(content={"similar_questions": similar_questions}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/answer")
async def answer(request: Request):
    try:
        data = request.json()
        domain = request.policy_id
        user_question = request.question

        # 데이터 불러오기
        df = pd.read_excel(f"./GW_FAQ.xlsx", sheet_name=domain - 1)

        # 사용자 질문과 일치하는 행 찾기
        matching_row = df[df['Q'] == user_question]

        # 일치하는 질문이 있는 경우
        if not matching_row.empty:
            # 일치하는 첫 번째 질문에 대한 답 출력
            matching_answer = matching_row.iloc[0]['A']
            return JSONResponse(content={"answer": matching_answer}, status_code=200)
        else:
            return JSONResponse(content={"error": "일치하는 질문이 없습니다."}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)