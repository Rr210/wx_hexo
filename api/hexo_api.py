# -*- coding: UTF-8 -*-
import json
from http.server import BaseHTTPRequestHandler
from hexo_re import Blog


def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]


def getdata(name):
    user_blog_link = 'https://rbozo.gitee.io'
    a = name   # 设置访问的页数
    if a == 1:
        url = user_blog_link
    else:
        url = '%s/page/%s' % (user_blog_link, a)
    print('---------------------------\n正在爬取第%s页' % a)
    return Blog(url).foreachs()


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        user = path.split('?')[1]
        data = getdata(user)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data,ensure_ascii=False).encode('utf-8'))
        return
