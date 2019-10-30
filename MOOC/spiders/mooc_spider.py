import scrapy
from MOOC.items import MoocItem
from MOOC.items import MlItem
import re

class Moocspider(scrapy.Spider):
    name = 'mooc'
    allowed_domains = ["mooc.org"]
    start_url = 'http://www.icourse163.org/learn/{}'
    resource_url = 'http://www.icourse163.org/dwr/call/plaincall/CourseBean.getLessonUnitLearnVo.dwr'
    HEAD = {
        # 'origin': 'https: // www.icourse163.org',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
    }
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
        self.course = [urls] if urls else [] # course 是一个列表包含所要下载课程id
        self.video = video # video=None 不下载视频， 0：标清（缺少异常处理）
        print("===================", self.course, self.video, "----------------")

    def start_requests(self): #开始遍历所有课程
        for url in self.course:
             yield scrapy.Request(self.start_url.format(url), headers=self.HEAD, callback=self.parse_basic)

    def parse_basic(self, response): # 获取课程基本信息
        content = response.xpath("//meta[@name= 'description']/@content").extract()[0].split(',')
        mt = {'name':content[1], 'school':content[2]}
        id = response.selector.re(r'id:(\d+),')[0]
        post_url = 'https://www.icourse163.org/dwr/call/plaincall/CourseBean.getLastLearnedMocTermDto.dwr'
        self.data1['c0-param0'] =  'number:' + id
        yield scrapy.FormRequest(post_url, meta=mt, headers=self.HEAD, formdata=self.data1,
                                 callback=self.parse_link,  dont_filter=True)

    def parse_link(self, response): # 获取各个资源的id
        s = response.text.encode('utf-8').decode('unicode_escape')
        chapter_pattern = r'homeworks=.*?;.+id=(\d+).*?name="(.*?)";'
        lesson_pattern = r'chapterId={}.*?contentId=null.*?contentType=1.*?id=(\d+).+name="(.*?)".*?'
        video_pattern = r'contentId=(\d+).+contentType=1.*?id=(\d+).*?lessonId={}.*?name="(.+)"'
        pdf_pattern = r'contentId=(\d+).+contentType=3.*?id=(\d+).*?lessonId={}.*?name="(.+)"'
        chapters = re.findall(re.compile(chapter_pattern), s)
        dc = dict()
        dc['name'], dc['shool'], dc['len'], dc['chapter'] = response.meta['name'], response.meta['school'], \
                                                            len(chapters), dict()
        for i, chapter in enumerate(chapters):
            chapter_id, chapter_name = chapter[0], chapter[1]
            lessons = re.findall(re.compile(lesson_pattern.format(chapter_id)), s)
            dc1 = dict()
            dc1['name'], dc1['len'], dc1['lesson'] = chapter_name, len(lessons), dict()
            for j, lesson in enumerate(lessons):
                lesson_id, lesson_name = lesson[0], lesson[1]
                videos = re.findall(re.compile(video_pattern.format(lesson_id)), s)
                dc2 = dict()
                dc2['name'], dc2['video_len'],  dc2['video'] = lesson_name, len(videos), dict()
                for k, video in enumerate(videos):
                    key = dict()
                    key['id'], key['name'] = video[1], video[2]
                    base = 'number:'
                    self.data2['c0-param0'], self.data2['c0-param1'], self.data2['c0-param3'] = \
                        base + video[0], base + '1', base + video[1]
                    name = [dc['name'], chapter_name, lesson_name, key['name']]
                    name = [it.replace(':','~') for it in name] # 文件夹的命名规范， 缺少异常处理
                    yield scrapy.FormRequest(self.resource_url, headers=self.HEAD, formdata=self.data2,
                                         meta={'type':'1', 'id':key['id'], 'name':name}, callback=self.parse, dont_filter=True)
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
                    name = [it.replace(':','~') for it in name]
                    yield scrapy.FormRequest(self.resource_url, headers=self.HEAD, formdata=self.data2,
                                             meta={'type': '3', 'id':key['id'], 'name':name}, callback=self.parse, dont_filter=True)
                    dc2['pdf'][k + 1] = key

                dc1['lesson'][j + 1] = dc2
            dc['chapter'][i + 1] = dc1
        item = MlItem()
        item['course'] = dc  # 将课程目录以json形式保存
        yield item

    def parse(self, response): # 根据资源id获取资源link
        item = MoocItem()
        dc = {'id':response.meta['id']}
        if response.meta['type'] == '1':
            pts = [r'mp4SdUrl="(.*?\.mp4).*?"',  r'mp4HdUrl="(.*?\.mp4)";',  'mp4ShdUrl="(.*?\.mp4)";']
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
            item['file_urls'] = []
            if self.video:
                item['file_urls'].append(self.video)
        item['file_name'] = response.meta['name']
        item['file_type'] = dc['type']
            # print(response.meta['name'])
            # print(dc[0])
            # input(">>>>")
        yield item


