import hashlib

class Encryption(object):
    """对password进行加密"""

    def __init__(self):
        pass

    @classmethod
    def md5(cls,requestData):

        if isinstance(requestData,dict):
            if "password" in requestData:
                password = requestData["password"]
                m5 = hashlib.md5()
                m5.update(password.encode("utf-8"))
                pwd = m5.hexdigest()
                requestData["password"] = pwd
                return requestData
            else:
                return None
        elif isinstance(requestData,str):
            k_v_str = requestData.split("&")
            k_v_dict = {}
            for i in k_v_str:
                k,v = i.split("=")
                k_v_dict[k] = v
            if "password" in k_v_dict:
                password = k_v_dict["password"]
                m5 = hashlib.md5()
                m5.update(password.encode("utf-8"))
                pwd = m5.hexdigest()
                k_v_dict["password"] = pwd
                reqData  = ""
                for k,v in k_v_dict.items():
                    reqData += k + "=" + v + "&"
                return reqData[:-1]
            else:
                return None

if __name__ == "__main__":
    requestData = '{"username":"lujingxia","password":"lujingxia123"}'
    requestData1 = 'username=lujingxia&password=lujingxia123'
    print(Encryption.md5(requestData1))