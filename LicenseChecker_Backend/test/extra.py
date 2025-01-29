import requests

headers = {
    'accept': 'application/json',
    # Already added when you pass json= but not when you pass data=
    # 'Content-Type': 'application/json',
}

json_data = [
    'MIT',
]

response = requests.post('http://127.0.0.1:8000/licenses/check/', headers=headers, json=json_data)
print(response.json())