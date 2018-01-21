import urllib.request, sys, base64, json, os, time, baiduSearch, threading
from PIL import Image, ImageEnhance
from common import config, screenshot
from aip import AipOcr
from tools import aitext

import re


# 词频显示

# 截图函数
def get_screenshot():
    #fname = './screenshot/2018-01-21-13-06-42.png'
    fname = screenshot.start_screenshot()
    # screenshot.pull_screenshot()
    print('采集图像：' + str(time.time() - start))
    im = Image.open(fname)  # 导入手机截图
    # 芝士超人
    region = im.crop((0, 340, 1080, 1190))  # 裁剪的区域,可以自己修改
    # 百万英雄
    # region = im.crop((0, 340, 1080, 1240))  # 裁剪的区域,可以自己修改
    # 冲顶大会
    #region = im.crop((0, 340, 1080, 1200))  # 裁剪的区域,可以自己修改
    img_size = region.size
    x_s = int(img_size[0] * 0.42)
    y_s = int(img_size[1] * 0.42)
    thumb = region.resize((x_s, y_s), Image.ANTIALIAS)
    thumb.save("./crop_test1.png")  # 提取题目截图


# 内容显示
def get_answer(issue):
    convey = 'n'
    if convey == 'y' or convey == 'Y':
        results = baiduSearch.search(issue, convey=True)
    elif convey == 'n' or convey == 'N' or not convey:
        results = baiduSearch.search(issue)
    else:
        print('输入错误')
        exit(0)

    count = 0
    max = 3
    for result in results:
        # print('{0} {1} {2} {3} {4}'.format(result.index, result.title, result.abstract, result.show_url, result.url))  # 此处应有格式化输出
        print('{0}'.format(result))  # 此处应有格式化输出
        count = count + 1
        if (count == max):  # 这里限制了只显示2条结果，可以自己设置
            break


def get_ai_answer(filePath):
    with open(filePath, 'rb') as fp:
        image = fp.read()
        respon = client.basicGeneral(image)
        titles = respon['words_result']  # 获取问题
        a_index = 99
        issue = ''
        answer = []
        for index, title in enumerate(titles):
            tmp = title['words']
            if (index > a_index):
                strinfo = re.compile('《|》|A\.|B\.|C\.|D\.|\(|\)')
                answer.append(strinfo.sub('', tmp))
            else:
                issue = issue + tmp
            if (tmp.endswith('?')):
                a_index = index
        if (len(issue) == 0):
            print('未发现可用信息')
            return
        if (issue.find('.') > -1 and issue.find('.') < 3):
            issue = issue[issue.find('.') + 1:]
        else:
            l = 0
            for i in range(len(issue)):
                if (i < 2):
                    if (str(issue[i]).isdigit()):
                        l += 1
                else:
                    break
            issue = issue[l:]
        print(issue, answer)  # 打印问题
        keyword = issue  # 识别的问题文本
        ai = aitext.Ai(issue, answer)
        if (ai.search() == False):
            get_answer(issue)


# 简易多线程
threads = []
t1 = threading.Thread(target=get_ai_answer, args=(r"./crop_test1.png",))
threads.append(t1)
# t2 = threading.Thread(target=get_answer, args=(r"./crop_test1.png",))
# threads.append(t2)
start = None
if __name__ == '__main__':

    # 导入配置百度ocr
    config = config.open_accordant_config()
    APP_ID = config['app_id']
    API_KEY = config['app_key']
    SECRET_KEY = config['app_secret']
    # 开始截图
    start = time.time()
    # 默认方式3截图,与系统有关,若多次check后方式为2,1,0请酌情于common/screenshot自行修改
    get_screenshot()
    # 调用baiduOCR识别
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    # get_ai_answer(r'./crop_test1.png')
    # get_answer(r'./crop_test1.png')
    # 启动多线程
    for t in threads:
        t.start()
    t.join()
    # 显示用时
    end = time.time()
    print('程序用时：' + str(end - start) + '秒')
