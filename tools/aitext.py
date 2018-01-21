import urllib.request, time, _thread, urllib.parse
from requests import get
from bs4 import BeautifulSoup


class Ai:

    def biggest(self, a, b, c, d):  # 获取出现次数最多的答案
        index = 0
        if a > b:
            maxnum = a
        else:
            maxnum = b
            index = 1
        if c > maxnum:
            maxnum = c
            index = 2
        if d > maxnum:
            maxnum = d
            index = 3
        return (maxnum, index)

    def parseHtml(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        elems = soup.find_all('div', attrs={'class': 'result', 'tpl': "se_com_default"})
        result = []
        for el in elems:
            result.append({'text': el.h3.a.getText(), 'link': el.h3.a['href']})
        print(result)
        # 匹配与问题匹配度最高的对象


    def __init__(self, issue, answer, merge=True):  # 注意前后各两个下划线
        self.start = time.time()
        self.issue = issue
        if (merge):
            for a in answer:
                self.issue = self.issue + ' ' + a
        self.answer = answer
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.count = 0
        self.winner = []

    def gethtml(self, url):  # 获取网页并统计词频
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}  # 构造头部
        # opener = urllib.request.build_opener()
        # opener.addheaders = [headers]
        # date = opener.open(url).read()
        r = get(url, headers=headers)
        if "zhidao.baidu.com/s" in url:
            r.encoding = 'gbk'
        str1 = r.text
        # if "zhidao.baidu.com/s" in url:
        #     print(str1)
        # if (str1 != None):
        #     print(str1)
        a = 0
        b = 0
        c = 0
        d = 0
        if (len(self.answer) > 0):
            a = str1.count(self.answer[0])
            self.a += a
        if (len(self.answer) > 1):
            b = str1.count(self.answer[1])
            self.b += b
        if (len(self.answer) > 2):
            c = str1.count(self.answer[2])
            self.c += c
        if (len(self.answer) > 3):
            d = str1.count(self.answer[3])
            self.d += d
        source = ''
        if "zhidao.baidu.com/s" in url:
            source = '百度知道'
        if "www.baidu.com" in url:
            source = '百度'
            #self.parseHtml(str1)
        if 'wenwen.sogou.com' in url:
            source = '搜狗问问'
        if 'cn.bing.com' in url:
            source = '必应'
        if 'www.so.com' in url:
            source = '360搜索'
        # print(source + '=>' + ' A:' + str(a) + ' B:' + str(b) + ' C:' + str(c) + ' D:' + str(d))
        self.count += 1
        self.winner.append(self.biggest(a, b, c, d))
        #  self.b += str1.count(self.answer[1].replace('B', ''))
        #  self.c += str1.count(self.answer[2].replace('C', ''))

    def threhtml(self, url):  # 开线程获得网页
        _thread.start_new_thread(self.gethtml, (url,))

    def search(self):  # 要搜索的引擎

        # 可以自己添加搜索接口
        baidubaike = self.threhtml(
            "https://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&ie=utf8&word=" + urllib.parse.quote(self.issue))
        baidu = self.threhtml("http://www.baidu.com/s?wd=" + urllib.parse.quote(self.issue))
        sousou = self.threhtml("http://wenwen.sogou.com/s/?w=" + urllib.parse.quote(self.issue) + "&ch=ww.header.ssda")

        # iask = self.threhtml(
        #    "https://iask.sina.com.cn/search?searchWord=" + urllib.parse.quote(self.issue) + "&record=1")
        bing = self.threhtml("https://cn.bing.com/search?q=" + urllib.parse.quote(self.issue))
        # so360 = self.threhtml("https://www.so.com/search/?q=" + urllib.parse.quote(self.issue))

        while 1:
            if (self.count > 3):
                break

        dict = {self.a: 'A', self.b: 'B', self.c: 'C', self.d: 'D'}
        if (self.a == 0 and self.b == 0 and self.c == 0 and self.d == 0):
            return False
        # str1=str(iask,"utf-8")
        listselect = [self.a, self.b, self.c, self.d]
        print('---------------------------------')
        print(' 选项    出现次数   结果')
        if (self.a > 0):
            print('  A：     ' + str(self.a) + '         ' + self.answer[0])
        if (self.b > 0):
            print('  B：     ' + str(self.b) + '         ' + self.answer[1])
        if (self.c > 0):
            print('  C：     ' + str(self.c) + '         ' + self.answer[2])
        if (self.d > 0):
            print('  D：     ' + str(self.d) + '         ' + self.answer[3])
        print('---------------------------------')
        result = self.biggest(self.a, self.b, self.c, self.d)
        print('  推荐答案：' + dict[result[0]] + '       ' + self.answer[result[1]])
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        for re in self.winner:
            if (re[1] == 0):
                self.a += 1
            if (re[1] == 1):
                self.b += 1
            if (re[1] == 2):
                self.c += 1
            if (re[1] == 3):
                self.d += 1
        result = self.biggest(self.a, self.b, self.c, self.d)
        # print(result)
        print('  出现频率：' + '       ' + self.answer[result[1]])
        print('---------------------------------')
        print()
        end = time.time()
        print('搜索用时：' + str(end - self.start) + '秒')
        return True
