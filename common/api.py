import json
import requests
from common.readexcel import ExcelUtil
from common.copy_excel import copy_excel,Write_excel
import os
from filecmp import cmp

def send_requests(s,testdata):
    '''封装requests请求'''
    method = testdata["method"]
    url = testdata["url"]
    try:
        params = eval(testdata["params"])
    except:
        params = None

    try:
        headers = eval(testdata["headers"])
        print("请求头部：s%" % headers)
    except:
        headers = None

    try:
        cookies = eval(testdata["cookies"])
    except:
        cookies = None


    type = testdata["type"]

    test_nub = testdata['id']
    print("*******正在执行用例：-----  %s  ----**********" % test_nub)
    print("请求方式：%s, 请求url:%s" % (method, url))
    print("请求params：%s" % params)

    # post请求body内容
    try:
        bodydata = eval(testdata["body"])
    except:
        bodydata ={}

    # 判断传data数据还是json
    if type == "json":
        body = json.dumps(bodydata)
    else:
        body = bodydata

    if method == "post":
        print("post请求body类型为: %s,body内容为: %s" % (type,body))

    verify = False
    res = {} #接收返回数据

    try:
        r = s.request(method=method,
                      url=url,
                      params=url,
                      headers=headers,
                      data=body,
                      verify=verify,
                      cookies=cookies
                      )
       # print("页面返回信息：%s" % r.content.decode("utf-8"))
        res["content"] = r.content.decode("utf-8")
        res["id"] = testdata["id"]
        res["rowNum"] = testdata["rowNum"]
        res["statuscode"] = str(r.status_code)
        res["text"] = r.content.decode("utf-8")
        res["times"] = str(r.elapsed.total_seconds())
        if res["statuscode"] !="200":
            res["error"] = res["text"]
        else:
            res["error"] = ""
        res["msg"] = ""
        res["result"] = "fail"
        if testdata["checkpoint"] in str(res["text"]):
            res["result"] = "pass"
            print("用例测试结果：%s------->%s" % (test_nub,res["result"]))
        return res
    except Exception as err:
        res["msg"] = str(err)
        return res


def write_result(result,filename):

    row_num = result["rowNum"]
    wt = Write_excel(filename)
    wt.write("I"+str(row_num),result["statuscode"])
    wt.write("J"+str(row_num),result["times"])
    wt.write("K"+str(row_num),result["error"])
    wt.write("M"+str(row_num),result["msg"])
    wt.write("L"+str(row_num),result["result"])
    wt.write("N"+str(row_num),result["content"])



if __name__ == "__main__":
    sheetName="Sheet1"
    current_path = os.path.dirname(os.path.realpath(__file__))
    testdate_path = os.path.join(os.path.dirname(current_path),"testdate")
    report_path = os.path.join(os.path.dirname(current_path),"report")
    filePath = os.path.join(testdate_path,"test.xlsx")
    filePath2 = os.path.join(report_path,"test_report.xlsx")
    #print(filePath)
    data = ExcelUtil(filePath,sheetName).dict_data()
    print(data[0])
    s = requests.session()
    res = send_requests(s, data[1])
    #print(res)
    copy_excel(filePath,filePath2)
    write_result(res,filePath2)








