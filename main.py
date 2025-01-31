import time
from typing import List

from fastapi import FastAPI, HTTPException, Request, Response, BackgroundTasks
from pydantic import HttpUrl
from schemas.request import PredictionRequest, PredictionResponse
from utils.logger import setup_logger


import requests

OAUTH_TOKEN = 'y0__xCe3sWiAhjB3RMgvq3ekxIZOoNJglVYAvEdl2yjfz1I9twJXQ'
FOLDER_ID = 'b1gelm71dtja21t76a4n'
IAM_TOKEN = None

def get_iam_token():
    global IAM_TOKEN
    url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
    data = {"yandexPassportOauthToken": OAUTH_TOKEN}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print(response)
        iam_token = response.json().get('iamToken')
        print(f"IamToken : {iam_token}")  
        IAM_TOKEN = iam_token
    else:
        print(f"err: {response.status_code}, {response.text}")
        


# Initialize
app = FastAPI()
logger = None


@app.on_event("startup")
async def startup_event():
    global logger
    logger = await setup_logger()
    get_iam_token()
    
    


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    body = await request.body()
    await logger.info(
        f"Incoming request: {request.method} {request.url}\n"
        f"Request body: {body.decode()}"
    )

    response = await call_next(request)
    process_time = time.time() - start_time

    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk

    await logger.info(
        f"Request completed: {request.method} {request.url}\n"
        f"Status: {response.status_code}\n"
        f"Response body: {response_body.decode()}\n"
        f"Duration: {process_time:.3f}s"
    )

    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
    )

from get_gpt_answer import getYandexGptAnswer
from get_search_answer import getYandexSearchAnswer


CREDITS = r"\n Ответ сгенерирован с помощью YandexGPT"

@app.post("/api/request", response_model=PredictionResponse)
async def predict(body: PredictionRequest):

    get_iam_token()
    try:
        # search_answer = getYandexSearchAnswer(IAM_TOKEN,FOLDER_ID, body.query)
        
        await logger.info(f"Processing prediction request with id: {body.id}")
        # Здесь вызов модели
        gpt_answer = getYandexGptAnswer(IAM_TOKEN,FOLDER_ID, body.query)
        answer = gpt_answer['answer'] if gpt_answer['answer'] !=-1 else None

        await logger.info(f"Yandex GPT answer: {gpt_answer}")


        sources: List[HttpUrl] = [
            HttpUrl(link) for link in gpt_answer['links']
        ]

        response = PredictionResponse(
            id=body.id,
            answer=answer,
            reasoning=gpt_answer['reasoning']+CREDITS,
            sources=sources,
        )
        await logger.info(f"Successfully processed request {body.id}")
        return response
    except ValueError as e:
        error_msg = str(e)
        await logger.error(f"Validation error for request {body.id}: {error_msg}")
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        await logger.error(f"Internal error processing request {body.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")






