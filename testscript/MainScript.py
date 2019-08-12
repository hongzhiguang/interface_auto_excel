from utils.ExcelParse import ExcelParse
from conf.ProjVar import *
from utils.HttpClient import *
from action.data_store import RelyDataStore
from action.get_rely import GetRelyData
from action.check_result import CheckResult
from action.encryption import Encryption
import re

testExcel = ExcelParse(testcase_path)

# 遍历API sheet
for cell in (testExcel.get_rows(API_active_col_no))[1:]:
    # 重新回到API sheet
    testExcel.set_sheet_by_name(API_sheet_name)
    if cell.value.lower() == "y":
        APIName = testExcel.get_cell_value(cell.row,API_apiName_col_no)
        requestUrl = testExcel.get_cell_value(cell.row,API_requestUrl_col_no)
        requestMethod = testExcel.get_cell_value(cell.row,API_requestMethod_col_no)
        paramType = testExcel.get_cell_value(cell.row,API_paramsType_col_no)
        APITestCase = testExcel.get_cell_value(cell.row,API_apiTestCase_col_no)
        print("------------%s------------" % APIName)

        # 遍历可执行的testcase
        testExcel.set_sheet_by_name(APITestCase)
        for cell in (testExcel.get_rows(CASE_active_col_no))[1:]:
            if cell.value.lower() == "y":
                requestData = testExcel.get_cell_value(cell.row,CASE_requestData_col_no)
                relyData = testExcel.getHttpClient_cell_value(cell.row,CASE_relyData_col_no)
                dataStore = testExcel.get_cell_value(cell.row,CASE_dataStore_col_no)
                checkPoint = testExcel.get_cell_value(cell.row,CASE_checkPoint_col_no)
                # print(requestData,relyData,dataStore,checkPoint)

                # 如果有数据依赖处理的话，先进行数据依赖处理，并获取到请求
                if relyData:
                    requestData = GetRelyData.get(requestData,relyData)
                else:
                    print("%s的第%s条不需要做数据依赖处理" % (APIName,cell.row-1))

                # if RequestData.startswith("{") and RequestData.endswith("}"):
                print(requestData)
                if requestData[0] == "{" and requestData[-1] == "}":
                    # 说明请求参数是一个json串格式数据
                    requestData = eval(requestData)

                # 如果请求的url为登录接口的url,需要对密码进行md5加密
                if re.search(r"login",requestUrl):
                    requestData = Encryption.md5(requestData)

                # 获取响应
                response = HttpClient.request(requestUrl,requestMethod,paramType,requestData)
                if response.status_code == 200:
                    # 获取接口响应的body
                    responseBody = response.json()
                    # 做数据依赖存储
                    if dataStore:
                        RelyDataStore.do(APIName,cell.row-1,requestData,responseBody,eval(dataStore))
                        print(REQUEST_DATA)
                        print(RESPONSE_DATA)
                    # 接下来进行接口响应结果检测
                    if checkPoint:
                        errorKey = CheckResult.check(response.json(),eval(checkPoint))
                    # 写响应结果，包括状态码和响应body
                    testExcel.write_cell(cell.row,CASE_responseCode_col_no,response.status_code)
                    testExcel.write_cell(cell.row,CASE_responseData_col_no,str(response.json()))
                    # 写校验结果，包括校验结果以及错误信息
                    if errorKey:
                        testExcel.write_cell(cell.row,CASE_status_col_no,"fail")
                        testExcel.write_cell(cell.row,CASE_errorInfo_col_no,str(errorKey))
                    else:
                        testExcel.write_cell(cell.row,CASE_status_col_no,"pass")
                else:
                    # 写响应结果，包括状态码和响应body
                    testExcel.write_cell(cell.row, CASE_responseCode_col_no, response.status_code)
                    testExcel.write_cell(cell.row, CASE_status_col_no, "fail")
            else:
                print("%s的第%s条case被忽略执行！" % (APIName,cell.row-1))
                continue
    else:
        print("第%s个API被忽略执行！" % (cell.row-1))

