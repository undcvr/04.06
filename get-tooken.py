import requests

url = "http://127.0.0.1:8000/api/token/"
# url = "http://127.0.0.1:8000/api-token-auth/"

r = requests.post(
    url,
    data={"username": "admin", "password": "admin"},
)

print(r.json())