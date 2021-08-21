# -*- coding:utf8 -*-
import requests, json, re
from lxml import etree

# 解决打印问题，默认关闭
import sys, io
sys.stdout = io.TextIOWrapper(buffer=sys.stdout.buffer, encoding='utf8')
# 定义最后的json数组
result_json = []
# 定义对象
results = {
    'title': '',
    "en_update_date": "",
    "update_date": "",
    "en_publish_date": "",
    "publish_date": "",
    "title_url": "",
    "article_category": "",
    "article_wordCounts": "",
    "read_time": "",
    "cover": "",
    "article_content": "",
}


def writer():
    with open('hexoapi.json', 'w', encoding='utf8') as f:
        json.dump(result_json, f, ensure_ascii=False)
    # f = open('hexo_api.json', mode='wb')
    # f.write(json.dump())


class Blog:
    def __init__(self, urls):
        self.url = urls
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4464.5 Safari/537.36'
        }

    # 请求页面信息

    def req(self, *args):
        page_urls = user_blog_link + args[0] if len(args) != 0 else self.url
        # 转换成二进制，解决xpath乱码的问题
        res = requests.get(page_urls, headers=self.header).content.decode('utf-8')
        return res

    # 对页面进行解析

    def etreehtml(self):
        # 匹配当前页面的正文信息
        content = re.findall('(<div class="recent-post-item">.*?</div></div></div>)', self.req())  # *?尽可能的少匹配字符，懒惰模式
        # print(content)
        return content

    # 解析子页面
    def childpage(self, child_url):
        text = re.search('<div id="post-meta">(?P<Gcon>.*?)</div></div>', self.req(child_url))
        publish = re.search('<time class="post-meta-date-created" datetime="(?P<Ctime>.*?)" title="(?P<unencode>.*?)">',
                            text.group('Gcon'))  # 发布时间
        update = re.search('<time class="post-meta-date-updated" datetime="(?P<Ctime>.*?)" title="(?P<unencode>.*?)">',
                           text.group('Gcon'))  # 更新时间
        word_count = re.search('<span class="word-count">(?P<wordCount>.*?)</span>', text.group('Gcon'))  # 文章字数
        read_t = re.search('<span class="post-meta-label">.*?</span><span>(?P<TR>.*?)</span></span>',text.group('Gcon'))
        results['en_publish_date'] = publish.group('Ctime')  # 转码时间
        results['publish_date'] = publish.group('unencode')  # 未经过转码时间
        results['en_update_date'] = update.group('Ctime')  # 未经过转码时间
        results['update_date'] = update.group('unencode')  # 未经过转码时间
        results['article_wordCounts'] = word_count.group('wordCount')  # 文章字数
        results['read_time'] = read_t.group('TR')  # 文章阅读时长
        try:
            article = re.search('<article class="post-content" id="article-container">(?P<articles>.*?)</article>', self.req(child_url))
            results['article_content'] = article.group('articles').replace('\"', "'")   # 文章内容
        except:
            results['article_content'] = '超出字符'  # 文章内容


    # 对页面的数据进行遍历处理
    def foreachs(self):
        print(len(self.etreehtml()))
        for i in self.etreehtml()[0:]:
            title = re.search(
                '<a href="(?P<link>.*?)" title="(?P<title>.*?)"><img class="post_bg".*?data-lazy-src="(?P<src>.*?)"',
                i)  # 文章的标题
            results['title'] = title.group('title')  # 文章标题
            results['cover'] = title.group('src')  # 图片地址
            results['title_url'] = title.group('link')  # 文章地址
            self.childpage(results['title_url'])
            result_json.append(dict(results))

    # 爬取页面的总页数
    def pagenum(self):
        lists = etree.HTML(self.req())
        content = lists.xpath('//*[@id="pagination"]/div/a[2]/text()')
        # print(content[0])
        return json.loads(content[0])


if __name__ == '__main__':
    # 调用类
    user_blog_link = 'https://rbozo.gitee.io'
    pageNum = Blog(user_blog_link).pagenum()
    for a in range(1, pageNum + 1):
        if a == 1:
            url = user_blog_link
        else:
            url = '%s/page/%s' % (user_blog_link, a)
        Blog(url).foreachs()
        print('---------------------------\n正在爬取第%s页' % a)
    print('---------------爬取完成------------------')
    print(result_json)
    writer()
