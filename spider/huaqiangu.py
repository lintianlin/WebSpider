# 从www.136book.com 获取花千骨小说
from urllib import request
from bs4 import BeautifulSoup

if __name__ == '__main__':
    url = 'http://www.136book.com/huaqiangu/'
    head = {}
    head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
    req = request.Request(url, headers=head)
    response = request.urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    soup_texts = soup.find('div', id='book_detail', class_='box1').find_next('div')
    # 打开文件
    f = open('F:/huaqiangu.txt', 'w')
    # 循环解析链接地址
    for link in soup_texts.ol.children:
        if link != '\n':
            download_url = link.a.get('href')
            download_req = request.Request(download_url, headers=head)
            download_response = request.urlopen(download_req)
            download_html = download_response.read()
            download_soup = BeautifulSoup(download_html, 'html.parser')
            download_soup_texts = download_soup.find('div', id='content')
            # 抓取其中文本
            download_soup_texts = download_soup_texts.text
            # 写入章节标题
            f.write(link.text + '\n\n')
            # 去除每一章底部的js代码
            startindex = download_soup_texts.find('document.write')
            download_soup_texts = download_soup_texts[:startindex]
            # 写入章节内容
            f.write(download_soup_texts)
            f.write('\n\n')
    f.close()