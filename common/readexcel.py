import xlrd
import os
import pandas as pd
import numpy as np

class ExcelUtil(object):

    def __init__(self,excelPath,sheetName='Sheet1'):
        self.data = xlrd.open_workbook(excelPath)
        self.table = self.data.sheet_by_name(sheetName)
        #获取第一行作为key值
        self.keys = self.table.row_values(0)
        #获取总行数
        self.rowNum = self.table.nrows
        #获取总列数
        self.colNum = self.table.ncols

    def dict_data(self):
        if self.rowNum <=1:
            print('总行数小于1')
        else:
            result = {}
            r=[]
            j=1
            for i in list(range(self.rowNum-1)):
                print("i:",i)
                s = {}
                #从第二行取对应values值
                s['rowNum'] = i+2
                values = self.table.row_values(j)
                for x in list(range(self.colNum)):
                    print("x:" ,x)
                    s[self.keys[x]] = values[x]
                r.append(s)
                print("r:" , r)
                j +=1
            data = pd.DataFrame(r)
            nameList = list(data["name"].drop_duplicates())

            for na in nameList:
                list_name =[]
                date_by_name = data[data["name"]==na]
                for index in date_by_name.index:
                    dict1 = dict(date_by_name.loc[index])
                    list_name.append(dict1)
                result[na] =list_name
            print(result)
            return result

if __name__=="__main__":

    sheetName="Sheet1"
    current_path = os.path.dirname(os.path.realpath(__file__))
    testdate_path = os.path.join(os.path.dirname(current_path),"testdate")
    report_path = os.path.join(os.path.dirname(current_path),"report")
    #print(current_path)
    #print(testdate_path)
    #print(report_path)
    filePath = os.path.join(testdate_path,"test.xlsx")
    #print(filePath)
    date = ExcelUtil(filePath,sheetName)
    print(date.dict_data())