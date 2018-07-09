import unittest
import ddt
import os
import requests
from common.copy_excel import copy_excel,Write_excel
from common.readexcel import ExcelUtil
from common.api import send_requests,write_result
import json

#读取test.xlsx文件中的测试数据
current_path = os.path.dirname(os.path.realpath(__file__))
testdata_path = os.path.join(os.path.dirname(current_path),"testdate")
testdatafile = os.path.join(testdata_path,"test.xlsx")
testdata = ExcelUtil(testdatafile).dict_data()

#复制测试数据至report目录下的report.xml文件中
report_path=os.path.join(os.path.dirname(current_path),"report")
reportfile =os.path.join(report_path,"report.xlsx")
copy_excel(testdatafile,reportfile)

#登录信息
loginData={"username":"xxxxxx","password":"yyyyyyy"}


@ddt.ddt
class Test_api(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #登录
        cls.s = requests.session()
        cls.s.request(method="",
                      url="",
                      data=loginData)

    @ddt.data(*testdata["A"])
    def test_A(self,data):
        #调用http接口
        res = send_requests(self.s,data)

        check = data["checkpoint"]

        #将结果写入report.xlsx中
        write_result(res,reportfile)

    @ddt.data(*testdata["B"])
    def test_B(self,data):
         #调用http接口
        res = send_requests(self.s,data)

        check = data["checkpoint"]

        #将结果写入report.xlsx中
        write_result(res,reportfile)

    def check(self,res,checkpoint):
        res_dict = eval(res['content'])
        check_dict = eval(checkpoint)
        print(str(res_dict))
        print(str(check_dict))
        self.assertEqual(res_dict['userDesc'],check_dict['userDesc'])
        self.assertEqual(res_dict["userType"],check_dict["userType"])
        self.assertEqual(res_dict["code"],check_dict["code"])
        self.assertEqual(res_dict["userName"],check_dict["userName"])

if __name__=="__main__":
    unittest.main()




