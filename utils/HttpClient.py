import requests
import json

class HttpClient(object):

    def __init__(self):
        pass

    @classmethod
    def request(cls,requestUrl,requestMethod,paramType,requestData=None,headers=None):
        if requestMethod == "post":
            if paramType == "form":
                # 使用form表单提交的方式
                response = requests.post(url=requestUrl,data=json.dumps(requestData),headers = headers)
                return response
            elif paramType == "json":
                # 使用json传参的方式
                response = requests.post(url=requestUrl,json=json.dumps(requestData),headers = headers)
                return response
        elif requestMethod == "get":
            if paramType == "url":
                # 说明参数是直接拼接在url上面的
                request_url = "%s%s" %(requestUrl,requestData)
                response = requests.get(request_url,headers=headers)
                return response
            elif paramType == "params":
                # 说明get请求传参是通过params参数接受的
                if isinstance(requestData,dict):
                    response = requests.get(requestUrl,params=json.dumps(requestData),headers=headers)
                else:
                    response = requests.get(requestUrl,params=requestData,headers=headers)
                return response

if __name__ == "__main__":
    requestUrl = "http://39.106.41.11:8080/register/"
    requestMethod = "post"
    paramsType = "form"
    requestData = {"username":"linwei", "password":"linwei123","email":"linwei@qq.com"}
    response = HttpClient.request(requestUrl,requestMethod,paramsType,requestData)
    print(response.status_code)
    print(response.json())


