
'''
课程搜索页面 https://www.imooc.com/search/course?words=python&page=2 words搜索关键字 page指第几页
'''
import os # 调用系统变量
import re # 正则表达式相关

import urllib
import urllib.request
import urllib.error
import urllib.parse

import json
import socket

import time

class ImoocSpider:
    
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    def getPythonHtml(self,keyWord,page='1'):
        myKeyWord = urllib.parse.quote(keyWord)
        searchUrl='https://www.imooc.com/search/course?words='+myKeyWord+'&page='+page
        try:
            request = urllib.request.Request(url=searchUrl, headers=self.headers) # 构建请求
            htmlPage = urllib.request.urlopen(request) 
            rsp = htmlPage.read().decode('utf-8')  # 指定编码格式
        except UnicodeDecodeError as e:
                print(e)
                print('-----UnicodeDecodeErrorurl:', searchUrl)
        except urllib.error.URLError as e:
                print(e)
                print("-----urlErrorurl:", searchUrl)
        except socket.timeout as e:
                print(e)
                print("-----socket timout:", searchUrl)
        else:
                self.saveFile(rsp,keyWord)
        finally:
                htmlPage.close()

    def saveFile(self,res,keyWord):
            b="./" + keyWord +'.txt'
            try :
                fp=open(b,'w',encoding='utf-8') 
                pattern = re.compile(r'<div.*?course-item.*?>.*?<a.*?course-detail-title.*?</a>.*?<div.*?course-item-detail.*?>.*?<a.*?highlight.*?>(.*?)</span>(.*?)</a>.*?<div.*?course-item-classify.*?>.*?<span>.*?<span>(.*?)<a.*?course-tname.*?>(.*?)</a>.*?</span>.*?<span>(.*?)</span>.*?</div>.*?<p>(.*?)<span.*?highlight.*?>(.*?)</span>(.*?)</p>.*?</div>.*?</div>',re.S)
                results=pattern.findall(res)
                for result in results:
                    flag=0
                    for r in result:
                        htmlTag=re.findall('<.*?>',r,re.S) # 判断有没有存在html标签的内容，如果有的话本条数据就不做写入  
                        if len(htmlTag)!=0:
                            flag=2
                            break 
                        else :
                            flag=1    
                    if flag!=2:
                        final_r=''
                        for r in result:
                            final_r=final_r+r.strip()  # r.strip()
                        print (final_r,file=fp)   
                        print ('写入+1')      
                    else :
                        print ('遇到未成功过滤的内容，不做写入')          
            except :
                    print('操作存在错误')
            finally :
                   fp.close()
                   print ('saveFile方法执行结束')
                   
  

    def start (self, keyWord):
        self.getPythonHtml(keyWord) 
    
    
if __name__ == '__main__':
    imoocInfo = ImoocSpider()
    imoocInfo.start('python')




    
