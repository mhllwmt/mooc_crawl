import requests
import os
#exec_str = r'copy /b  ts/c9645620628078.ts+ts/c9645620628079.ts  ts/1.ts'
#os.system(exec_str)
with open('test.txt', 'r', encoding='utf') as f:
    cookie = f.read()
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

url = 'https://www.icourse163.org/web/j/resourceRpcBean.getResourceToken.rpc?csrfKey=f5bca95f91044895af65fa6fb6c82035'
response = requests.post(url, headers=head, data=data)
input(response.json())
x = response.json()
signature = x['result']['videoSignDto']['signature']
videoId = x['result']['videoSignDto']['videoId']
name = x['result']['lessonUnitName']
# ts 名字
url1 = 'https://vod.study.163.com/eds/api/v1/vod/video?videoId={}&signature={}&clientType=1'.format(videoId, signature)

x = requests.get(url1).json()
video_url = x['result']['videos'][0]['videoUrl']
m3u8 = requests.get(video_url)
txt = m3u8.text.split('\n')
urls = []
for it in txt:
    if 'EXT' not in it and '.ts' in it:
        urls.append(it)
pos1 = video_url.rfind('/')
pos2 = video_url.rfind('?')
ts_url = video_url[:pos1+1]+'{}'+video_url[pos2:]
for it in urls:
    # print(ts_url.format(urls[0]))
    ts = requests.get(ts_url.format(it)).content
    with open('.\\ts\\'+it, 'wb') as f:
        f.write(ts)

shell_str = r'copy /b .\ts\*.ts .\ts\mt.mp4'
os.system(shell_str)
