# Финальный проект в мегашколе ИТМО 2024 трек ИИ
### Необходимо было  разработать агента, который будет предоставлять информацию об Университете ИТМО.

Для создания Api был использован FastAPI, в качестве Api к LLM был использован [Yandex GPT API](https://yandex.cloud/ru/services/yandexgpt)

Приложение развернуто по адресу: [147.45.232.168](http://147.45.232.168)    

Его API:
Метод POST - получить ответ на вопрос в формате JSON  
URL: [147.45.232.168/api/request](147.45.232.168/api/request) + json




## Инструкция по сборке
Для запуска выполните команду:

```bash
docker-compose up -d
```
Она соберёт Docker-образ, а затем запустит контейнер.

## Проверка работы
Отправьте POST-запрос на эндпоинт /api/request. Например, используйте curl:

```bash
curl --location --request POST 'http://147.45.232.168/api/request' \
--header 'Content-Type: application/json' \
--data-raw '{
  "query": "В каком городе находится главный кампус Университета ИТМО?\n1. Москва\n2. Санкт-Петербург\n3. Екатеринбург\n4. Нижний Новгород",
  "id": 1
}'
```
В ответ вы получите JSON вида:

```json
{
  "id": 1,
  "answer": 1,
  "reasoning": "Из информации на сайте",
  "sources": [
    "https://itmo.ru/ru/",
    "https://abit.itmo.ru/"
  ]
}
```



![Пример](https://github.com/Summit2/ITMO-Agent/blob/master/example.png)



Чтобы остановить сервис, выполните:

```bash
docker-compose down
```



