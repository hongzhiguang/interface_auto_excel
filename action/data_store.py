from conf.ProjVar import REQUEST_DATA,RESPONSE_DATA

class RelyDataStore(object):

    def __init__(self):
        pass

    @classmethod
    def do(cls,APIName,caseID,requestData,responseBody,dataStore):
        # 当请求参数使用的是表单的str，需要统一转成dict
        requestData_dict = {}
        if isinstance(requestData,str):
            for i in requestData.split("&"):
                k0,v0 = i.split("=")
                requestData_dict[k0] = v0
            requestData = requestData_dict
        # 遍历dataStore，判断存储的数据是request还是response
        for k,v in dataStore.items():
            if k == "request":
                # 说明需要存储的来自于接口的请求参数
                for i in v:
                    if i in requestData:
                        # 第一次存储数据REQUEST_DATA={"register":{"1":{"username":""}}}
                        if APIName not in REQUEST_DATA:
                            REQUEST_DATA[APIName] = {str(caseID):{i:requestData[i]}}
                        else:
                            # 添加新的caseID
                            if str(caseID) not in REQUEST_DATA[APIName]:
                                REQUEST_DATA[APIName][str(caseID)] = {i:requestData[i]}
                            else:
                                # 添加与username同等级的password等
                                REQUEST_DATA[APIName][str(caseID)][i] = requestData[i]
                    else:
                        print("需要做数据依赖存储的参数%s不存在" % i)
            elif k == "response":
                # 说明需要存储的依赖数据是来自接口的响应body
                for i in v:
                    if i in responseBody:
                        # 第一次存储数据RESPONSE_DATA={"register":{"1":{"userid":""}}}
                        if APIName not in RESPONSE_DATA:
                            RESPONSE_DATA[APIName] = {str(caseID):{i:responseBody[i]}}
                        else:
                            # 添加新的caseID
                            if str(caseID) not in RESPONSE_DATA[APIName]:
                                RESPONSE_DATA[APIName][str(caseID)] = {i:responseBody[i]}
                            else:
                                # 添加与userid同等级的token等
                                RESPONSE_DATA[APIName][str(caseID)][i] = responseBody[i]
                    else:
                        print("需要存储的依赖参数%s在响应body中未找到" % i)

        return REQUEST_DATA,RESPONSE_DATA


if __name__ == "__main__":
    APIName = "register"
    caseID = "2"
    requestData = {"username": "linwei", "password": "linwei123", "email": "linwei@qq.com"}
    responseBody = {"code": "00", "userid": 357}
    dataStore = {"request":["username","password"],"response":["userid"]}
    RelyDataStore.do(APIName,caseID,requestData,responseBody,dataStore)










