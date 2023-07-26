import requests

url = "http://127.0.0.1:8000/books/"

# headers = {
#     "Authorization": "Token 57a28f481045cc3fd6a45b73735215767f4a112f"
# }

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg0NzQxNTA3LCJpYXQiOjE2ODQ3Mzc5MDcsImp0aSI6Ijg0NTU0YWVmMzdlNzQxODI4ODk0YzM2Zjc1NTQzZmU0IiwidXNlcl9pZCI6MX0.l--3sq__HEeu5s6db4VWtsDhMNB_0PSUoITmIlP9r_U"
}

r = requests.get(url, headers=headers)

print(r.json())
