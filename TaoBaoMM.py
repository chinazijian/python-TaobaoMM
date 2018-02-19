# -*- coding: UTF-8 -*- 

import urllib.request
import simplejson as json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Spider:
    def __init__(self):
        self.InitialURL= r'https://mm.taobao.com/alive/list.do'


    def getPage(self,PageIndex):
        url=self.InitialURL+'''?scene=all&page='''+str(PageIndex)+'''&callback=jsonp191'''
        print(url+r'\n')
        request=urllib.request.Request(url)
        request.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36') #否则会被淘宝ban
        response=urllib.request.urlopen(request)
        return response.read().decode('gbk')

    def getContents(self,PageIndex):
        page=self.getPage(PageIndex)
        self.JsonObject=json.loads(page[13:-1])#去除头尾不必要字符串读取json并转换为python对象
        logger.debug(self.JsonObject)
        for item in self.JsonObject["dataList"]:
           # logger.info(type(item))
            dictItem={} #以字典形式保存,方便后续操作
            for subItem in item.items():
               dictItem[str(subItem[0])]=str(subItem[1])
               logger.debug(dictItem)
            imgUrl=r'http'+dictItem['avatarUrl']
            #nickName=dictItem['darenNick']
            #description=dictItem['desc']
            #profileH5Url=r'http'+dictItem['profileUrlH5']
            #profilePCUrl=r'http'+dictItem['profileUrlPc']
            #UserID=dictItem['userId']
                
                

    def saveImg2Disk(self,dictItem):
        pass

    def saveDict2Xls(self,dictTtem):
        pass

    

if __name__=='__main__':
    spider=Spider()
    spider.getContents(2)