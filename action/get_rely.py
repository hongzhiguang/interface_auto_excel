from conf.ProjVar import RESPONSE_DATA,REQUEST_DATA

class GetRelyData(object):

    def __init__(self):
        pass

    @classmethod
    def get(cls,requestData,relyData):
        if not requestData or not relyData:
            return None
        # 如果请求参数是json类型，使用eval转换成功，如果是字符串，会报语法错误
        try:
            reqData = eval(requestData)
        except SyntaxError as er:
            reqData = requestData

        if relyData:
            relyData = eval(relyData)

        # 遍历依赖数据
        if isinstance(reqData,dict):
            for k,v in relyData.items():
                # 请求的参数值来自于所依赖的接口请求参数值
                if k == "request":
                    for k1,v1 in v.items():
                        interfaceName,caseID = v1.split("->")
                        try:
                            if k1 in REQUEST_DATA[interfaceName][caseID]:
                                val = REQUEST_DATA[interfaceName][caseID][k1]
                                reqData[k1] = val
                        except KeyError as err:
                            print("%s字段不再存储的数据中" % k1)
                # 请求的参数值来自于所依赖的接口响应参数值
                elif k == "response":
                    for k1,v1 in v.items():
                        interfaceName, caseID = v1.split("->")
                        try:
                            if k1 in RESPONSE_DATA[interfaceName][caseID]:
                                val = RESPONSE_DATA[interfaceName][caseID][k1]
                                reqData[k1] = val
                        except KeyError as err:
                            print("%s字段不再存储的数据中" % k1)
            return str(reqData)
        else:
            # 说明请求参数是字符串类型，类似于get请求时直接将参数拼接到url上
            k_v_str = requestData.split("&")
            k_v_dict = {}
            # 将str转成dict
            for i in k_v_str:
                print(i)
                key,value = i.split("=")
                k_v_dict[key] = value
            for k,v in relyData.items():
                # 请求的参数值来自于所依赖的接口请求参数值
                if k == "request":
                    for k1,v1 in v.items():
                        interfaceName, caseID = v1.split("->")
                        try:
                            if k1 in REQUEST_DATA[interfaceName][caseID]:
                                val = REQUEST_DATA[interfaceName][caseID][k1]
                                k_v_dict[k1] = val
                        except KeyError as err:
                            print("%s字段不再存储的数据中" % k1)

                # 请求的参数值来自于所依赖的接口响应参数值
                elif k == "response":
                    for k1,v1 in v.items():
                        interfaceName, caseID = v1.split("->")
                        try:
                            if k1 in RESPONSE_DATA[interfaceName][caseID]:
                                val = RESPONSE_DATA[interfaceName][caseID]
                                k_v_dict[k1] = val
                        except KeyError as err:
                            print("%s字段不再存储的数据中" % k1)
            reqDataStr = ""
            for k,v in k_v_dict.items():
                reqDataStr += k + "=" + v + "&"
            return reqDataStr[:-1]


if __name__ == "__main__":
    REQUEST_DATA = {'register': {'2': {'username': 'linwei', 'password': 'linwei123'}}}
    RESPONSE_DATA = {'register': {'2': {'userid': 357}}}
    requestData = {"username":"","password":""}
    requestData1 = 'username=&password='
    relyData1 = {"request":{"username":"register->2","password":"register->2"}}
    print(GetRelyData.get(str(requestData),str(relyData1)))