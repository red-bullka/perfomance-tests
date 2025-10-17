import httpx

response = httpx.get("https://jsonplaceholder.typicode.com/todos/1")

print(response.status_code)
print(response.json())


data = {
    "title": "Новая задача",
    "completed": False,
    "user_id": 1
}
response = httpx.post("https://jsonplaceholder.typicode.com/todos")

print(response.status_code)
print(response.json())

headers = {"Authorization": "Bearer my_secret_token"}
response = httpx.get("https://httpbin.org/get", headers=headers)

print(response.status_code)
print(response.json())