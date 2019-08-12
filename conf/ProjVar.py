import os

# 工程所在的目录
proj_path = os.path.dirname(os.path.dirname(__file__))

# 测试用例所在的绝对路径
testcase_path = os.path.normpath(os.path.join(proj_path,"data",u"测试用例.xlsx"))

# API相关所在的列
API_sheet_name = "API"
API_apiName_col_no = 2
API_requestUrl_col_no = 3
API_requestMethod_col_no = 4
API_paramsType_col_no = 5
API_apiTestCase_col_no = 6
API_active_col_no = 7

# 测试用例相关所在的列
CASE_requestData_col_no = 1
CASE_relyData_col_no = 2
CASE_responseCode_col_no = 3
CASE_responseData_col_no = 4
CASE_dataStore_col_no = 5
CASE_checkPoint_col_no = 6
CASE_active_col_no = 7
CASE_status_col_no = 8
CASE_errorInfo_col_no = 9

# 存储请求参数里面依赖数据
REQUEST_DATA = {}

# 存储响应对象中的依赖数据
RESPONSE_DATA = {}




