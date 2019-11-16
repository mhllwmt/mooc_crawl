import copy
import json
import os
import re

import scrapy

from MOOC.items import MlItem
from MOOC.items import MoocItem
from MOOC.items import TsItem

with open('test.txt', 'r', encoding='utf') as f:
    cookie = f.read()


class Moocspider(scrapy.Spider):
    name = 'mooc'
    # allowed_domains = ["mooc.org"]
    start_url = 'http://www.icourse163.org/learn/{}'
    info_url = 'https://www.icourse163.org/course/{}'
    resource_url = 'http://www.icourse163.org/dwr/call/plaincall/CourseBean.getLessonUnitLearnVo.dwr'
    HEAD = {
        # 'origin': 'https: // www.icourse163.org',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
    }
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        # 'accept-encoding': 'gzip, deflate, br',
        # 'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
        # 'content-type' : 'application/x-www-form-urlencoded',
        'cookie': cookie,
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        # 'origin':'https://www.icourse163.org',
        # 'referer':'https://www.icourse163.org/learn/ZJU-1003377027?tid=1206951274'
    }
    data = {
        'bizId': '1215050852',
        'bizType': '1',
        'contentType': '1'
    }
    _url = 'https://www.icourse163.org/web/j/resourceRpcBean.getResourceToken.rpc?csrfKey=f5bca95f91044895af65fa6fb6c82035'
    data1 = {
        'callCount': '1',
        'scriptSessionId': '${scriptSessionId}190',
        'c0-scriptName': 'CourseBean',
        'c0-methodName': 'getMocTermDto',
        'c0-id': '0',
        'c0-param0': 'number:',
        'c0-param1': 'number:1',
        'c0-param2': 'boolean:true',
        'batchId': '1492167717772'
    }
    data2 = {
        'callCount': '1',
        'scriptSessionId': '${scriptSessionId}190',
        'httpSessionId': '79c8ef666c024d298f69898f1cc03ecc',
        'c0-scriptName': 'CourseBean',
        'c0-methodName': 'getLessonUnitLearnVo',
        'c0-id': '0',
        'c0-param0': 'number:597004',
        'c0-param1': 'number:3',
        'c0-param2': 'number:0',
        'c0-param3': 'number:1215166139',
        'batchId': '1571924896605'
    }

    def __init__(self, urls=None, video=None, *args, **kwargs):
        super(Moocspider, self).__init__(*args, **kwargs)
        # self.course = ['ZJU-93001']
        self.course = urls if urls else []  # course 是一个列表包含所要下载课程id
        self.video = video  # video=None 不下载视频， 0：标清（缺少异常处理）

    def start_requests(self):  # 开始遍历所有课程
        for url in self.course:
            yield scrapy.Request(self.start_url.format(url), headers=self.HEAD, meta={'id': url},
                                 callback=self.parse_basic)

    def parse_basic(self, response):  # 获取课程基本信息
        content = response.xpath("//meta[@name= 'description']/@content").extract()[0].split(',')
        mt = {'name': content[1], 'school': content[2], "id": response.meta['id']}
        id = response.selector.re(r'id:(\d+),')[0]
        post_url = 'https://www.icourse163.org/dwr/call/plaincall/CourseBean.getLastLearnedMocTermDto.dwr'
        self.data1['c0-param0'] = 'number:' + id
        yield scrapy.FormRequest(post_url, meta=mt, headers=self.HEAD, formdata=self.data1,
                                 callback=self.parse_link, dont_filter=True)

    def parse_link(self, response):  # 获取各个资源的id
        s = response.text.encode('utf-8').decode('unicode_escape')
        chapter_pattern = r'homeworks=.*?;.+id=(\d+).*?name="(.*?)";'
        lesson_pattern = r'chapterId={}.*?contentId=null.*?contentType=1.*?id=(\d+).+name="(.*?)".*?'
        video_pattern = r'contentId=(\d+).+contentType=1.*?id=(\d+).*?lessonId={}.*?name="(.+)"'
        pdf_pattern = r'contentId=(\d+).+contentType=3.*?id=(\d+).*?lessonId={}.*?name="(.+)"'
        chapters = re.findall(re.compile(chapter_pattern), s)
        dc = dict()
        dc['ml'] = dict()
        dc['name'], dc['shool'], dc['ml']['len'], dc['ml']['chapter'] = response.meta['name'], response.meta['school'], \
                                                                        len(chapters), dict()
        for i, chapter in enumerate(chapters):
            # if i==1:   break
            # Hi 这是我最后改动的地方~~~再见^^ m't
            chapter_id, chapter_name = chapter[0], chapter[1]
            lessons = re.findall(re.compile(lesson_pattern.format(chapter_id)), s)
            dc1 = dict()
            dc1['name'], dc1['len'], dc1['lesson'] = chapter_name, len(lessons), dict()
            for j, lesson in enumerate(lessons):
                # @目的 debug第5.3节课
                lesson_id, lesson_name = lesson[0], lesson[1]
                videos = re.findall(re.compile(video_pattern.format(lesson_id)), s)
                dc2 = dict()
                dc2['name'], dc2['video_len'], dc2['video'] = lesson_name, len(videos), dict()
                for k, video in enumerate(videos):
                    key = dict()
                    key['id'], key['name'] = video[1], video[2]
                    base = 'number:'
                    self.data2['c0-param0'], self.data2['c0-param1'], self.data2['c0-param3'] = \
                        base + video[0], base + '1', base + video[1]
                    name = [dc['name'], chapter_name, lesson_name, key['name']]
                    name = [it.replace(':', '~') for it in name]  # 文件夹的命名规范， 缺少异常处理
                    yield scrapy.FormRequest(self.resource_url, headers=self.HEAD, formdata=self.data2,
                                             meta={'type': '1', 'id': key['id'], 'name': name}, callback=self.parse,
                                             dont_filter=True)
                    dc2['video'][k + 1] = key
                pdfs = re.findall(re.compile(pdf_pattern.format(lesson_id)), s)
                dc2['pdf_len'], dc2['pdf'] = len(pdfs), dict()
                for k, pdf in enumerate(pdfs):
                    key = dict()
                    key['id'], key['name'] = pdf[1], pdf[2]
                    base = 'number:'
                    self.data2['c0-param0'], self.data2['c0-param1'], self.data2['c0-param3'] = \
                        base + pdf[0], base + '3', base + pdf[1]
                    name = [dc['name'], chapter_name, lesson_name, key['name']]
                    name = [it.replace(':', '~') for it in name]
                    yield scrapy.FormRequest(self.resource_url, headers=self.HEAD, formdata=self.data2,
                                             meta={'type': '3', 'id': key['id'], 'name': name}, callback=self.parse,
                                             dont_filter=True)
                    dc2['pdf'][k + 1] = key
                dc1['lesson'][j + 1] = dc2
                # break
            dc['ml']['chapter'][i + 1] = dc1
            # break
        item = MlItem()
        item['course'] = dc
        yield scrapy.Request(self.info_url.format(response.meta['id']), meta={'item': item}, headers=self.HEAD,
                             callback=self.parse_info)

    def parse_info(self, response):
        dc = dict()
        item = response.meta['item']
        txt = response.xpath("//div[@id='j-rectxt']/text()").extract()[0]
        dc['课程详情'] = txt
        dt1 = response.xpath("//div[@class='category-title f-f0']").xpath('string(.)')
        dt2 = response.xpath("//div[@class='category-content j-cover-overflow']").xpath('string(.)')
        for i in range(len(dt1)):
            name = dt1[i].extract().strip('\n').replace('\xa0', ' ')
            txt = dt2[i].extract().strip('\n').replace('\xa0', ' ')
            if len(txt):
                dc[name] = txt
        tr = ['lectorPhoto', 'lectorName ', 'lectorTitle ']
        teachers = []
        pattern = r'{}: "(.*?)"'
        for it in tr:
            ans = re.findall(re.compile(pattern.format(it)), response.text)
            if not len(teachers):
                for x in ans:
                    tmp = {it: x}
                    teachers.append(tmp)
            else:
                for i, x in enumerate(ans):
                    teachers[i][it] = x
        dc['teachers'] = teachers
        item['course'].update(dc)
        yield item

    def parse(self, response):  # 根据资源id获取资源link
        item = MoocItem()
        dc = {'id': response.meta['id']}
        if response.meta['type'] == '1':
            pts = [r'mp4SdUrl="(.*?\.mp4).*?"', r'mp4HdUrl="(.*?\.mp4)";', 'mp4ShdUrl="(.*?\.mp4)";']
            dc['type'] = 'video'
            for i, pt in enumerate(pts):
                ans = re.search(pt, response.text)
                dc[i] = ans.group(1) if ans else ''
        else:
            pt = 'textOrigUrl:"(.*?)"'
            ans = re.search(pt, response.text).group(1)
            dc['type'] = 'pdf'
            dc[0] = ans

        item['file_urls'] = [dc[0]]
        if dc['type'] == 'video':
            # 字幕
            srt_pt = r's0.url="(.*?)"'
            ans = re.search(srt_pt, response.text)
            url = ans.group(1) if ans else ''
            srtitem = MoocItem()
            srtitem['file_name'] = response.meta['name']
            srtitem['file_type'] = 'srt'
            srtitem['file_urls'] = [url]
            yield srtitem

            item['file_urls'] = []
            if self.video != None :
                if dc[self.video] == '' :
                    # True 默认所有的视频文件全部以ts格式爬取
                    # 这样貌似不行哎
                    self.data['bizId'] = response.meta['id']
                    name = response.meta['name']
                    yield scrapy.FormRequest(self._url, method='POST', headers=self.head, formdata=self.data,
                                             meta={'name': name}, callback=self.parse_video, dont_filter=True)
                    # response = requests.post(self._url, headers=self.head, data=self.data)
                    # input(response.json())
                    return
                else:
                    item['file_urls'].append(dc[self.video])
        item['file_name'] = response.meta['name']
        item['file_type'] = dc['type']
        yield item

    def parse_video(self, response):
        x = json.loads(response.text)
        signature = x['result']['videoSignDto']['signature']
        videoId = x['result']['videoSignDto']['videoId']
        url = 'https://vod.study.163.com/eds/api/v1/vod/video?videoId={}&signature={}&clientType=1'.format(videoId,
                                                                                                           signature)
        name = response.meta['name']
        yield scrapy.Request(url, meta={'name': name}, callback=self.parse_video1)

    def parse_video1(self, response):
        x = json.loads(response.text)
        url = x['result']['videos'][self.video]['videoUrl']
        name = response.meta['name']
        yield scrapy.Request(url, meta={'name': name}, callback=self.parse_video2)

    def parse_video2(self, response):
        url = response.url
        txt = response.text.split('\n')
        urls = []
        pos1 = url.rfind('/')
        pos2 = url.rfind('?')
        name = response.meta['name']
        name[-1] = name[-1].replace(' ', '').strip('.')
        num = 0
        for i, it in enumerate(txt):
            if 'EXT' not in it and '.ts' in it:
                urls.append(it)
                txt[i] = name[-1] + '{}.ts'.format(str(num))
                num += 1
        ts_url = url[:pos1 + 1] + '{}' + url[pos2:]
        item = TsItem()
        for i, it in enumerate(urls):
            item['file_urls'] = [ts_url.format(it)]
            tmp = copy.copy(name)
            tmp[-1] = name[-1] + str(i)
            item['file_name'] = tmp
            yield item
        ml = '../data/{}/{}/{}'.format(name[0], name[1], name[2])
        if not os.path.exists(ml):
            os.makedirs(ml)
        with open('../data/{}/{}/{}/{}.m3u8'.format(*name), 'w', encoding='utf') as f:
            f.write("\n".join(txt))

#   ffmpeg -i hello.m3u8 -vcodec copy -acodec copy media.mp4
