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

@ddt.ddt
class Test_api(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.s = requests.session()
        #在这里登录

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
        res_dict = eval(res)
        check_dict = eval(checkpoint)

        self.assertEqual(res_dict[""],check_dict[""],)

if __name__=="__main__":
    unittest.main()




