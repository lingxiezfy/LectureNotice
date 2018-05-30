import requests
import re
import os
import smtplib
from bs4 import BeautifulSoup

from email.mime.text import MIMEText

urlHead = "http://news.nchu.edu.cn/"

f = open('讲座.txt', 'a')
f.close()

fin = open('讲座.txt', 'r')
list = fin.readlines()
fin.close()

def getHTMLText(url):
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return ""


def getContent(url):
    html = getHTMLText(url)
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find(id="myTab0_Content1")
    str = ''
    links = content.find_all("a", text=re.compile("卧龙创客大讲堂|卧龙人生+"))
    for link in links:
        name = link.get_text()+'\n'
        try:
           index = list.index(name)
        except:
            with open('讲座.txt', 'a') as f:
                f.write(name)
            str += '<a href="'+urlHead
            str += link.get('href')+'" target="_blank">'
            str += link.get_text()+'</a> <br/>'
    if len(str) > 0 :
        send_mail(str)
    
def send_mail(content):
    _user = "保密"
    _pwd  = "保密"
    _to   = "1241948182@qq.com"

    msg = MIMEText(content,"html","utf-8")
    msg["Subject"] = "讲座通知"
    msg["From"]    = _user
    msg["To"]      = _to

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(_user, _pwd)
        s.sendmail(_user, _to, msg.as_string())
        s.quit()
        print("Success!")
    except smtplib.SMTPException :
        print ("Falied!")


def main():
    url = "http://news.nchu.edu.cn/index.aspx"
    getContent(url);

main()
