import requests
import json

url = "http://39.106.41.11:8080/register/"
data = {"username":"luxiaoxia","password":"luxiaoxia123","email":"luxiaoxia@qq.com"}
response = requests.post(url=url,data=json.dumps(data))
print(response.status_code)