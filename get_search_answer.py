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

#     url = 'https://searchapi.api.cloud.yandex.net/v2/web/searchAsync'
#     data = {
#     "query": {
#       "searchType": "SEARCH_TYPE_RU",
#       "queryText": query,
#       "familyMode": "FAMILY_MODE_MODERATE",
#       "page": "1"
#     },
#     "sortSpec": {
#       "sortMode": "SORT_MODE_BY_RELEVANCE",
#       "sortOrder": "SORT_ORDER_DESC"
#     },
#     "groupSpec": {
#       "groupMode": "GROUP_MODE_DEEP",
#       "groupsOnPage": "3",
#     #   "docsInGroup": "3"
#     },
#     # "maxPassages": "3",
#     # "region": "65",
#     "l10N": "LOCALIZATION_RU",
#     "folderId": folder_id
# }
#     headers = {"Authorization": f"Bearer {iam_token}"}
#     response = requests.post(url, json=data, headers=headers)
#     if response.status_code == 200:
#         response_json =  response.json()
        
#         # result = json.loads(response_json)
#         print(response)
#         # return result
#     else:
#         print(f"err: {response.status_code}, {response.text}")
#         return None