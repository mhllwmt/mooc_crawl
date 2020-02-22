# mooc_crawler
An implementation of BIT-IR final project crawler part
中国大学MOOC 基于scrapy 的多线程爬虫

## introduction
   * 基于scrapy的多线程爬虫，爬虫资资源-中国大学MOOC
   * 爬取资源以文件夹子节点组织为树形结构
   * 文件资源不仅局限于视频，课件，字母，还包括课程介绍
   * 视频文件以ts流形式下载，并利用ffmpeg无损合并视频，请提前装好ffmpeg，并加入环境变量中
   * 如果无法爬取视频，可尝试更新cookies.txt
## get start
   * 运行main.py, 输入课程id,默认下载北京理工大学python程序设计
