import requests, json
from lxml import etree

# 定义最后的json数组
result_json = []
# 定义对象
results = {
    'title': '',
    "publish_date": "",
    "update_date": "",
    "article_content": "",
    "article_category": "",
    "article_wordCounts": "",
    "read_time": "",
    "cover": ""
}


def writer():
    with open('hexo_api.json', 'w', encoding='utf8') as f:
        json.dump(result_json, f, ensure_ascii=False)


class Blog:
    def __init__(self, url):
        self.url = url
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4464.5 Safari/537.36'
        }

    # 请求页面信息

    def req(self):
        # 转换成二进制，解决xpath乱码的问题
        res = requests.get(self.url, headers=self.header).content
        return res

    # 对页面进行解析

    def etreehtml(self):
        lists = etree.HTML(self.req())
        content = lists.xpath(
            '//*[@id="recent-posts"]/*[@class="recent-post-item"]')
        return content

    # 对页面的数据进行遍历处理

    def foreachs(self):
        # 加一个判断条件如果说遍历的是第一页，则从第二个开始
        # article =
        for i in self.etreehtml()[2:]:
            title = i.xpath('div[2]/a/@title')[0]  # 文章的标题
            publish_date = i.xpath(
                'div[2]/div[1]/*[@class="post-meta-date"]/time/@datetime')[0]  # 文章的发布时间
            article_category = i.xpath(
                'div[2]/div[1]/*[@class="article-meta"]/a/text()')[0]  # 文章的分类
            # cover = i.xpath('div[1]/a/img/@src')[0]   # 文章封面图
            # print(cover)
            # results['cover'] = cover
            results['title'] = title
            results['publish_date'] = publish_date
            results['article_category'] = article_category
            # 将对象转换成字典的形式在追加到数组中
            result_json.append(dict(results))

    # 爬取页面的总页数
    def pagenum(self):
        lists = etree.HTML(self.req())
        content = lists.xpath('//*[@id="pagination"]/div/a[2]/text()')
        # print(content[0])
        return content[0]


if __name__ == '__main__':
    # 调用类
    pageNum = Blog('https://rbozo.gitee.io/').pagenum()
    for a in range(1, pageNum):
        if a == 1:
            url = 'https://rbozo.gitee.io/'
        else:
            url = 'https://rbozo.gitee.io/page/%s' % a
        # print(url)
        print('---------------------------\n正在爬取第%s页' % a)
        Blog(url).foreachs()
    print('---------------爬取完成------------------')
    print(result_json)
    writer()
