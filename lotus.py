# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import re
import codecs
strhead='''
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title></title>
</head>
<body>
 '''
strfoot='''
</body>
</html>
'''
def outRuby(list1,list2,n):
    print(len(list1))
    print(len(list2))
    prelengthzi=0
    filename="Section"+n+".xhtml"
    print("reading to write "+filename)
    fout=codecs.open(filename,'w','utf-8')
    # fout = open(filename, "w")
    fout.writelines(strhead)
    for vzi in list1:
        vpy=list2[list1.index(vzi)]
        vpy_array=vpy.split("|")
        # print(vzi+vpy+" 对比"+str(len(vzi))+":"+len(vpy.split("|")).__str__())
        if len(vzi)==len(vpy_array):
            if list1.index(vzi)>0:
                prelengthzi=len(list1[list1.index(vzi)-1])
            if len(vzi)<=14 and prelengthzi<14:
                # print("<p>")
                fout.writelines("<p>")
            for i in range(0,len(vzi)):
                if(len(vpy_array[i].strip())!=0):
                    # print("<ruby>"+vzi[i]+"<rt>"+vpy_array[i]+"</rt></ruby>")
                    fout.writelines("<ruby>"+vzi[i]+"<rt>"+vpy_array[i]+"</rt></ruby>")
                else:
                    fout.writelines(vzi[i])
                    # print(vzi[i])
            if len(vzi)<14:
                # print("</p>")
                fout.writelines("</p>")
        else:
            if vzi==vpy:
                print(vzi)
            else:
                print("ERROR"+vzi+vpy+" is not same length")
    print(filename+" write complete")
    fout.close()
def genURLFromNumber():
    pre_str="http://www.fotuozhengfa.com/chaojing/lotus-sutra-"
    urls=[]
    for i in range(1,29):
        urls.append(pre_str+i.__str__())
    return urls
def fetchURL(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    req=urllib.request.Request(url,headers=hdr)
    response = urllib.request.urlopen(req)
    soup =BeautifulSoup(response,"html.parser")
    alljp=soup.find_all("p", class_="jp")
    allpp=soup.find_all("p", class_="pp")
    reschinese='[\u4e00-\u9fa5]'
    list1=[]
    list2=[]
    for jp in alljp:
        for zi in jp.find_all("span"):
            list1.append(zi.text)
    for pp in allpp:
        for py in pp.find_all("span"):
            list2.append(py.text)
    lianjielist=[]
    lianjielist.append(list1)
    lianjielist.append(list2)
    return lianjielist




def getAndReplaceLine(teststr):
    res='[\u4e00-\u9fa5]\([a-zà-ǜ|　|]+\)'
    result=re.findall(res,teststr)
    # print(result)
    re.sub(res,"m",teststr)
    for v in result:
        if teststr.find("<ruby>"+v+"</ruby>")==-1:
            teststr=teststr.replace(v,"<ruby>"+v+"</ruby>")
    return teststr

def writeFile():
    f = open("mflh 2.txt","r")
    fout = open("out.txt", "w")
    lines = f.readlines()

    for line in lines:
        s="<p>"
        s+=getAndReplaceLine(line)
        s+="</p>"
        fout.write(s)
    f.close()
    fout.close()
# teststr="妙(miào)法(fǎ)莲(lián)华(huá)经(jīng)序(xù)品(pǐn)第(dì)一(yī),"
# print(teststr.find("妙s"))
# print(getAndReplaceLine(teststr))

lurl=genURLFromNumber()
for url in lurl:
    # lzipy=fetchURL(url)
    n=lurl.index(url)
    print("gurl"+url+"...")
    inputurl=url
    if(n==24):
        inputurl="http://www.fotuozhengfa.com/chaojing/pumenpin"
    lzipy=fetchURL(inputurl)
    if(len(lzipy)==2):
        outRuby(lzipy[0],lzipy[1],(n+1).__str__().zfill(4))