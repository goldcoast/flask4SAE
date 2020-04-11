# fetch Img Src From WX 
# tait
# 2020.03.30


from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import re
import random
import traceback


app = Flask(__name__)

# app.debug = True

#uer_agent库，随机选取，防止被禁
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4084.0 Safari/537.36"
]

def getHtmlContent(url):
    headers = {'user-agent':random.choice(USER_AGENT_LIST)}
    try:
        r = requests.get(url=url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        # print('.... {}'.format(r.text))
        return BeautifulSoup(r.content, 'lxml')
    except Exception:
        print('**** info: getHtmlContent occured Exceptions:')
        traceback.print_exc()

# 获取 URL 中的图片地址
def fetchImgSrc(url):
    imgSrcArray = []
    imgDicList = []
    try:
        soup = getHtmlContent(url)
        content_div = soup.find("div", attrs={"id": "js_content"})
        imgDicList = content_div.find_all("img")
    except Exception:
        traceback.print_exc()

    if(len(imgDicList) > 0):
        for imgs in imgDicList: 
            imgSrcArray.append(imgs["data-src"])
    
    return imgSrcArray
# 


@app.route('/')
def index():
    return '<h1>hello world</h1>'

# 测试地址
@app.route('/hi/<name>', methods=['get'])
def hello(name):
    obj_json = {"name": name}
    return jsonify(obj_json)


@app.route('/get/src', methods=['get'])
def parseImgs():
    url = request.args.get("url")
    srcList = {"imgSrcArray": fetchImgSrc(url)}
    return jsonify(srcList)

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5050
    )
    # url = 'https://mp.weixin.qq.com/s/sJ6nUP5HCyIsfXhhEpgNFQ'
    # fetchImgSrc(url)
