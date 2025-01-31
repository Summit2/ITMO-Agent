
import requests
import json

def getYandexGptAnswer(iam_token,folder_id, question):
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    data = {
        "modelUri": f"gpt://{folder_id}/yandexgpt-lite",
        "completionOptions":    {
            "stream": False,
            "temperature": 0.1,
            "maxTokens": "200"
            },
        "messages" : [
        {
            "role": "system",
            "text": r"""Дай номер правильного ответа на вопрос из списка ответов. Коротко поясни причину выбора своего ответа. Затем приведи до 3 реальных ссылок.\n
            Формат ответа - json. Пример: {answer : <твой ответ>, reasoning: <пояснение причины твоего ответа>, links: [link1, ...]} '\n
            Если вопрос без пунктов, то в ответе поставь -1 (answer : -1) """,
        },
        {
            "role": "user",
            "text": question,
        },
    ]
    }
    headers = {"Content-Type": "application/json", 
               "Authorization": f"Bearer {iam_token}"}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        response_json =  response.json()
        # print(response_json)
        raw_json_string = response_json["result"]["alternatives"][0]["message"]["text"]
        clean_json_string = raw_json_string.strip("```").strip()
        result = json.loads(clean_json_string)
        print(result)
        if isinstance(result['answer'], int)==False:
            result['answer']=-1
        return result
    else:
        print(f"err: {response.status_code}, {response.text}")
        return None


