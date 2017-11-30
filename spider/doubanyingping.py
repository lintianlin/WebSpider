# 分析豆瓣中最新电影的影评

from urllib import request
from bs4 import BeautifulSoup
import re
import jieba #分词包
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
 
import matplotlib
matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)
from wordcloud import WordCloud#词云包


resp = request.urlopen('https://movie.douban.com/nowplaying/hangzhou/')
html_data = resp.read().decode('utf-8')
soup = BeautifulSoup(html_data,'html.parser')
nowplaying_movie = soup.find_all('div',id = 'nowplaying')
nowplaying_movie_list = nowplaying_movie[0].find_all('li',class_ = 'list-item')

nowplaying_list = []
for item in nowplaying_movie_list:
    nowplaying_dict = {}
    nowplaying_dict['id'] = item['data-subject']
    for tag_img_item in item.find_all('img'):
        nowplaying_dict['name'] = tag_img_item['alt']
        nowplaying_list.append(nowplaying_dict)

requrl = 'https://movie.douban.com/subject/%s/comments?start=0&limit=20' % nowplaying_list[0]['id']
print(requrl)
resp2 = request.urlopen(requrl)
html_data2 = resp2.read().decode('utf-8')
soup2 = BeautifulSoup(html_data2,'html.parser')
comment_div_list = soup2.find_all('div',class_ = 'comment')
print(comment_div_list)
eachCommentList = []
for item in comment_div_list:
    if item.find_all('p')[0].string is not None:
        eachCommentList.append(item.find_all('p')[0].string)

print(eachCommentList)

comments = ''
for k in range(len(eachCommentList)):
    comments = comments + (str(eachCommentList[k])).strip()

print(comments)

pattern = re.compile(r'[\u4e00-\u9fa5]+')
filterdata = re.findall(pattern,comments)
print(filterdata)
cleaned_comments = ''.join(filterdata)
print(cleaned_comments)

segment = jieba.lcut(cleaned_comments)
words_df = pd.DataFrame({'segment':segment})
words_stat.head()

stopwords=pd.read_csv("F:\python\WebSpider\stopwords.txt",index_col=False,quoting=3,sep="\t",names=['stopword'], encoding='utf-8')#quoting=3全不引用
words_df=words_df[~words_df.segment.isin(stopwords.stopword)]
words_stat.head()



# 词云显示
wordcloud=WordCloud(font_path="F:\python\WebSpider\simhei.ttf",background_color="white",max_font_size=80) #指定字体类型、字体大小和字体颜色
word_frequence = {x[0]:x[1] for x in words_stat.head(1000).values}
word_frequence_list = []
for key in word_frequence:
    temp = (key,word_frequence[key])
    word_frequence_list.append(temp)
 
wordcloud=wordcloud.fit_words(word_frequence_list)
plt.imshow(wordcloud)

