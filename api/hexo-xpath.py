import requests, json
from lxml import etree

# ��������json����
result_json = []
# �������
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

    # ����ҳ����Ϣ

    def req(self):
        # ת���ɶ����ƣ����xpath���������
        res = requests.get(self.url, headers=self.header).content
        return res

    # ��ҳ����н���

    def etreehtml(self):
        lists = etree.HTML(self.req())
        content = lists.xpath(
            '//*[@id="recent-posts"]/*[@class="recent-post-item"]')
        return content

    # ��ҳ������ݽ��б�������

    def foreachs(self):
        # ��һ���ж��������˵�������ǵ�һҳ����ӵڶ�����ʼ
        # article =
        for i in self.etreehtml()[2:]:
            title = i.xpath('div[2]/a/@title')[0]  # ���µı���
            publish_date = i.xpath(
                'div[2]/div[1]/*[@class="post-meta-date"]/time/@datetime')[0]  # ���µķ���ʱ��
            article_category = i.xpath(
                'div[2]/div[1]/*[@class="article-meta"]/a/text()')[0]  # ���µķ���
            # cover = i.xpath('div[1]/a/img/@src')[0]   # ���·���ͼ
            # print(cover)
            # results['cover'] = cover
            results['title'] = title
            results['publish_date'] = publish_date
            results['article_category'] = article_category
            # ������ת�����ֵ����ʽ��׷�ӵ�������
            result_json.append(dict(results))

    # ��ȡҳ�����ҳ��
    def pagenum(self):
        lists = etree.HTML(self.req())
        content = lists.xpath('//*[@id="pagination"]/div/a[2]/text()')
        # print(content[0])
        return content[0]


if __name__ == '__main__':
    # ������
    pageNum = Blog('https://rbozo.gitee.io/').pagenum()
    for a in range(1, pageNum):
        if a == 1:
            url = 'https://rbozo.gitee.io/'
        else:
            url = 'https://rbozo.gitee.io/page/%s' % a
        # print(url)
        print('---------------------------\n������ȡ��%sҳ' % a)
        Blog(url).foreachs()
    print('---------------��ȡ���------------------')
    print(result_json)
    writer()
