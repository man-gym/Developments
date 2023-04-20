import requests
import json

# создание объекта JSON
data = {
    "username": "player123",
    "score": 100,
    "level": 5
}

json_data = json.dumps(data)

url = "http://game-server.com/api/scores"
headers = {'Content-type': 'application/json'}
response = requests.post(url, data=json_data, headers=headers)

if response.status_code == 200:
    print("Результат отправлен успешно!")
else:
    print("Ошибка отправки результата: ", response.status_code)
