import requests

url = "http://127.0.0.1:8000//api/users/3"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOnsiZW1haWwiOiJzdHJpbmcxIiwiaWQiOjN9LCJleHAiOjE3NDc1NjgxNTB9.Db7MPVdF0UbFyD6oXli0bfU9Oz-Cwinhe24npZ-RU5Y"
}

response = requests.get(url, headers=headers)
print(response.json())