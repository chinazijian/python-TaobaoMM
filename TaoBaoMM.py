# -*- coding: UTF-8 -*- 

import urllib.request
import socket
import simplejson as json
import logging
import openpyxl as xls
import re
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
socket.setdefaulttimeout(10) #设置默认等待时间，超过继续下一条 ,防止被tb禁

class Spider:
    def __init__(self):
        self.InitialURL= r'https://mm.taobao.com/alive/list.do'


    def getPage(self,PageIndex):
        url=self.InitialURL+'''?scene=all&page='''+str(PageIndex)+'''&callback=jsonp191'''
        print(url+r'\n')
        request=urllib.request.Request(url)
        request.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36') #否则会被淘宝ban
        response=urllib.request.urlopen(request)
        content = response.read().decode('gbk')
        response.close() #防止被tb禁
        time.sleep(0.5)#防止被tb禁
        return content

    def getContents(self,PageIndex):
        page=self.getPage(PageIndex)
        self.JsonObject=json.loads(page[13:-1])#去除头尾不必要字符串读取json并转换为python对象
        logger.debug(self.JsonObject)
        MMs=[]#保存该页所有MM
        for item in self.JsonObject["dataList"]:
            dictItem={} #以字典形式保存,方便后续操作
            for subItem in item.items(): #json返回的datalist字典，每一项都是包含2个数据项的元组组成的列表
               dictItem[str(subItem[0])]=str(subItem[1])
               logger.debug(subItem)
            dictItem['avatarUrl']=self.checkImgURL(dictItem['avatarUrl']) #规范化URL链接
            dictItem['profileUrlH5']=r'http'+dictItem['profileUrlH5']
            dictItem['profileUrlPc']=r'http'+dictItem['profileUrlPc']
            self.checkDictItem(dictItem)
            MMs.append(dictItem)
        self.saveMMs2Xls(MMs)
    
    #检查dict是否缺少项
    def checkDictItem(self,dictItem):
        keys=[]
        keys2=['avatarUrl','darenNick','desc','profileUrlH5','profileUrlPc','userId']
        for key,value in dictItem.items():
            keys.append(key)
        if len(keys) ==len(keys2): #比较原关键字列表与正确关键字列表是否长度相等，若一样则表示没有缺少
            return
        else:
            for i in range(0,len(keys2)): #循环比较两个列表
               if keys[i] == keys2[i]:
                   pass
               else:
                  lackKey=keys2[i]  #记录原列表缺少的项
                  dictItem[lackKey]=' ' #在字典中新增缺少的项，并赋值为空
                  keys.insert(i,lackKey) #在源关键字列表中缺漏的位置插入所缺关键字，其余项向后移动
            return

    def checkImgURL(self,url):
        pattern = re.compile(r'^http:')
        match = pattern.search(url)
        if match:
            logger.info(match.group())
            return url 
        else:
            return r'http:'+url

    def saveImg2Disk(self,MMs):
        pass

    def saveMMs2Xls(self,MMs):
        wb=xls.load_workbook(r"./淘宝MM信息表.xlsx")
        ws=wb.active #获取_active_sheet_index指定的表，默认第0个 
        for row in MMs:
            ws.append([row['avatarUrl'],row['darenNick'],row['desc'],row['profileUrlH5'],row['profileUrlPc'],row['userId']])
        wb.save('淘宝MM信息表.xlsx')

    def initXLS(self,wbName):
        wb=xls.Workbook();
        ws=wb.active
        ws.title="MM信息" #可以通过wb.get_sheet_by_name()获取表
        cellName=['照片链接','名字','描述','H5详情页链接','PC详情页链接','用户ID']
        ws.append(cellName)
        wb.save(wbName)
        logger.info("新建xlsx文件成功")

    

if __name__=='__main__':
    spider=Spider()
    spider.initXLS("淘宝MM信息表.xlsx")
    for page in range(1,67):
        spider.getContents(page)