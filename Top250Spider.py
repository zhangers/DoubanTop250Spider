#-*- coding = utf-8 -*-
import sys
import os
import re
import urllib
import urllib.request
import xlwt
from bs4 import BeautifulSoup



def main():
    #1,爬取网页
    baseurl="https://movie.douban.com/top250?start="
    datalist=getData(baseurl)
    savepath =".\\TOP250.xls"
    saveData(datalist,savepath)

    #askurl("https://movie.douban.com/top250?start=0")

findLink =re.compile(r'<a href="(.*?)">')  #创建正则表达式，表示字符串的模式
findName =re.compile(r'<img alt="(.*?)"')
findScore =re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findNumber=re.compile(r'<span>(.*?)人评价</span>')
findMember=re.compile(r'<p class="">(.*)<br/>',re.S)
findTime=re.compile(r'<br/>(.*)<div class="star">',re.S)
findInq=re.compile(r'<span class="inq">(.*?)。</span>',re.S)


#1,爬取网页
def getData(baseurl):
    datalist=[]
    for i in range(0,10):
        url=baseurl+str(i*25)
        askurl(url)
        html=askurl(url)        #save
        #2，逐一解析数据
        soup=BeautifulSoup(html,"html.parser")
        for item in soup.find_all("div",class_="item"): #查找符合要求的字符串并形成列表
            #print(item)    #查看电影全部信息
            data=[]     #保存一部电影的所有信息
            item = str(item)
            link=re.findall(findLink,item)[0]   #re库通过正则表达式查找字符串
            data.append(link)
            #print(link)
            name=re.findall(findName,item)[0]   #re库通过正则表达式查找字符串
            data.append(name)
            #print(name)
            score=re.findall(findScore,item)[0]   #re库通过正则表达式查找字符串
            data.append(score)
            #print(score)
            number=re.findall(findNumber,item)[0]   #re库通过正则表达式查找字符串
            data.append(number)
            #print(number)
            member=re.findall(findMember,item)[0]   #re库通过正则表达式查找字符串
            data.append(member.strip())
            #print(member.strip())
            time=re.findall(findTime,item)[0]
            time=re.sub('</p>',' ',time)
            time=re.sub('/',' ',time)
            data.append(time.strip())
            #print(time.strip())
            inq=re.findall(findInq,item)
            if len(inq)!=0:
                inq=inq[0].replace("。","")  #去掉句号
                data.append(inq)
            #print(inq)

            datalist.append(data)   #把处理好的一部电影放入Datalist
    #print(datalist)
    return datalist

#得到指定一个url的网页内容
def askurl(url):
    head={
        "User-Agent":" Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 70.0.3538.102Safari / 537.36Edge / 18.18363"
    }#伪装成浏览器
    request=urllib.request.Request(url,headers=head)
    html=""
    try:
        response=urllib.request.urlopen(request)
        html=response
        html.encoding="utf-8"
        #print(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)

    return html




#保存数据
def saveData(datalist,savepath):
    workbook = xlwt.Workbook(encoding='utf-8',style_compression=0)
    worksheet = workbook.add_sheet('sheet1',cell_overwrite_ok=True)
    col = ("详情链接", "影片名", "观众评分", "评价人数", "导演及主演", "时间&国籍&主题", "简评")
    for i in range(0, 7):
        worksheet.write(0, i, col[i])  # 列名
    for i in range(0,250):
        print("第%d条" %i)
        data=datalist[i]
        for j in range(0,7):
            worksheet.write(i+1,j,data[j])
    workbook.save(savepath)







if __name__ == "__main__":
#调用函数
    main()