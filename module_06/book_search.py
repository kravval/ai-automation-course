import requests

url = "https://openlibrary.org/search.json"
params = {"q": "python", "limit": 10}

response = requests.get(url, params)

print("Status code:", response.status_code)
print("Content type:", response.headers.get("Content-Type"))
print("Первые 300 символов ответа:")
print(response.text[:300])