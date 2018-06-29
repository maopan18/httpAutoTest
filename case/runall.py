import unittest
import time
from common import HTMLReport
import os

current_path = os.path.dirname(os.path.realpath(__file__))
report_path=os.path.join(os.path.dirname(current_path),"report")
if not os.path.exists(report_path): os.mkdir(report_path)
case_path = os.path.join(current_path, "case")

def add_case(casepath=current_path, rule="test*.py"):
    '''加载所有的测试用例'''
    discover = unittest.defaultTestLoader.discover(casepath,pattern=rule)

    return discover

def run_case(all_case,reportpath=report_path):
    '''执行所有的用例, 并把结果写入测试报告'''
    htmlreport=reportpath+r"\result.html"
    print("测试报告生成地址：%s" % htmlreport)
    fp = open(htmlreport,"wb")
    runner = HTMLReport.HTMLTestRunner(stream=fp,verbosity=2,title="测试报告",description="用例执行情况")
    runner.run(all_case)
    fp.close()

if __name__ =="__main__":
    cases = add_case()
    run_case(cases)
