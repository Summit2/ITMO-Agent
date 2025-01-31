from yandex_cloud_ml_sdk import YCloudML
import requests
import json

def getYandexSearchAnswer(iam_token,folder_id, query):
    url = f"https://yandex.ru/search/xml?folderid={folder_id}&apikey={iam_token}&query={requests.utils.quote(query)}&l10n=ru&sortby=rlv&filter=moderate&groupby=attr%3Dd.mode%3Ddeep.groups-on-page%3D3.docs-in-group%3D1&page=0"

    headers = {"Authorization": f"Bearer {iam_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            print(data)
            results = data.get("results", {}).get("grouped", [])
            
            links = []
            for group in results[:3]:  # Берем только первые 3 группы
                docs = group.get("docs", [])
                if docs:
                    links.append(docs[0].get("url"))  # Получаем первую ссылку в группе
            
            return links
        except (ValueError, KeyError) as e:
            print(f"Ошибка обработки ответа: {e}")
            return None
    else:
        print(f"Ошибка {response.status_code}: {response.text}")
        return None
