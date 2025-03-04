import json
import time
#selenium浏览器库
from selenium import webdriver
#爬虫所需库
from bs4 import BeautifulSoup
import jieba
from collections import Counter
import wordcloud
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rc("font",family='Microsoft YaHei')
browser_path = r"C:\Users\w163n\Desktop\python\chromedriver-win64\chromedriver.exe"
option = webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
#option.add_argument('User-Agent=Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36') # type: ignore
browser = webdriver.Chrome(browser_path,chrome_options=option)

print('BROWSER CREATED SUCCESSFULLY!')

def Get_Cookies(url = 'https://passport.weibo.com/sso/signin?entry=miniblog&source=miniblog&url='):
    browser.get(url)
    input('Press any keys once you have logged in!')
    with open('cookies.txt', 'w') as f:
        f.write(json.dumps(browser.get_cookies()))
        f.close()
    browser.quit()
        
def Weibo_Spider(keyword, page_num):
    #载入cookie条目
    browser1 = webdriver.Chrome(browser_path,chrome_options=option)
    browser1.get('https://passport.weibo.com/sso/signin?entry=miniblog&source=miniblog&url=')
    browser1.delete_all_cookies()
    with open('cookies.txt', 'r') as f:
        ck_lst = json.load(f)
        for ck_it in ck_lst:
            if isinstance(ck_it.get('expiry'), float):
                ck_it['expiry'] = int(ck_it['expiry'])
            browser1.add_cookie(ck_it)
    browser1.refresh()
    data = []
    for page in range(1, page_num + 1):
        url = f"https://s.weibo.com/weibo?q={keyword}&page={page}"
        browser1.get(url)
        browser1.implicitly_wait(2)
        soup = BeautifulSoup(browser1.page_source, "html.parser")
        a = soup.find_all('a')
        for ax in a:
            ax.clear()
        tweets = soup.find_all("p",{'node-type':'feed_list_content'})
        for tweet in tweets:
            data.append(tweet.text)
    return data

def process_data(data):
    text = "".join(data)
    words = jieba.lcut(text)
    words = [word for word in words if len(word) > 1]
    counts = Counter(words)
    return counts

def visualize_data(counts):
    # 词云
    wc = wordcloud.WordCloud(font_path="simhei.ttf", width=800, height=400)
    wc.generate_from_frequencies(counts)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()

    # 词频图
    top_words = counts.most_common(20)
    words, freqs = zip(*top_words)
    plt.bar(words, freqs)
    plt.xticks(rotation=90)
    plt.show()

Get_Cookies()
data = Weibo_Spider('国产游戏 传统文化', 100)
counts = process_data(data)
visualize_data(counts)