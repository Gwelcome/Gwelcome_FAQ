# Gwelcome_FAQ
Gwelcome_FAQ는 자주 묻는 질문(FAQ)에 대한 답변을 찾기 위한 모듈입니다.
## 개요
사용자로부터 policy_id와 question을 입력받아 해당정책 내에서 입력받은 질문과 유사한 질문 3개를 도출하여 사용자에게 반환합니다. 이후 3개의 질문 중 사용자가 선택한 질문에 대해 FAQ데이터를 바탕으로 답(answer)을 반환합니다.
# 서버 실행
''' uvicorn main:app --reload '''

# API 엔드포인트
## /top3 : 사용자 질문에 대해 가장 유사한 3개의 질문을 반환합니다.
''' {"policy_id": 1, "question": "사용자의 질문 입력"} '''
## /answer : 사용자 질문과 일치하는 답변을 반환합니다.
''' {"policy_id": 1, "question": "사용자의 질문 입력"} '''

# 데이터 구조
## FAQ데이터 : 'GW_FAQ.xlsx' 파일에 저장된 각 도메인별 FAQ 데이터를 활용합니다.

# 모델 및 라이브러리
## Sentence Transformer 모델 : Huffon/sentence-klue-roberta-base을 사용하여 문장 임베딩을 수행합니다.
