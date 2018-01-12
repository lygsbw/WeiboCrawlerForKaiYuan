# coding: utf-8
import re
from scrapy import FormRequest
from scrapy.spiders import BaseSpider
from scrapy.http import Request
from WeiboCrawler.items import SearchWeiboItem
from bs4 import BeautifulSoup
import datetime
import sys
import locale


class Spider(BaseSpider):
    name = "searchCrawler"
    host = "http://weibo.cn"

    def start_requests(self):
        # 关键字获取
        keyword = raw_input('Please input the keyword(s): ').decode(
            sys.stdin.encoding or locale.getpreferredencoding(True))
        # 时间获取
        endtime = raw_input('Please input the end time: ')
        endtime = datetime.datetime.strptime(endtime, '%Y%m%d')
        # 天数获取
        days = raw_input('Please input the days: ')
        oneDay = datetime.timedelta(days=1)
        for i in range(int(days)):
            starttime = endtime
            # 模拟浏览器
            postData = {
                'keyword': keyword,
                'smblog': '%E6%90%9C%E7%B4%A2',
                'advancedfilter': '1',
                'nick': '',
                'starttime': starttime.strftime('%Y%m%d'),
                'endtime': endtime.strftime('%Y%m%d'),
                'sort': 'time'}
            # print postData
            searchURL = 'https://weibo.cn/search/'
            yield FormRequest(url=searchURL, formdata=postData, callback=self.parseSearch, meta={"keyword": keyword})

            endtime = endtime - oneDay

    def parseSearch(self, response):
        """
        获取微博信息
        :param response: 从服务端发来的response
        :return: 一条完整的微博信息
        """
        soup = BeautifulSoup(response.text, "lxml")
        body = soup.body
        weiboList = body.find_all(attrs={'class': 'c'})
        for weibo in weiboList:

            weiboItem = SearchWeiboItem()

            # 如果这个div中包含原文内容的话
            if weibo.find(attrs={'class': 'ctt'}):

                weiboItem["Keyword"] = response.meta["keyword"]

                weiboItem["_id"] = weibo.attrs["id"]

                weiboItem["UserName"] = weibo.find(attrs={'class': 'nk'}).text

                # 获取内容
                content = weibo.find(
                    attrs={'class': 'ctt'}).text.strip().replace('\n', '')
                # print weiboItem["Content"].encode('gb18030')
                weiboItem["Content"] = content if content[
                    0] != ':' else content[1:]    # 去除冒号

                # 获取转发时间
                pubTime_tool = weibo.find(attrs={'class': 'ct'})
                pubTime_tool = pubTime_tool.text.strip().replace('\n', '').split(u'来自')
                time = pubTime_tool[0].strip()
                now = datetime.datetime.now()
                if time[:2] == u'今天':
                    # print time[2:].encode('gb18030')
                    weiboItem["PubTime"] = now.strftime('%Y-%m-%d ') + time[2:]
                elif time[-3:] == u'分钟前':
                    minutes = datetime.timedelta(minutes=int(time[:-3]))
                    weiboItem["PubTime"] = (
                        now - minutes).strftime('%Y-%m-%d %H:%M:%S')
                elif u'月' in time and u'日' in time:
                    weiboItem["PubTime"] = now.strftime(
                        '%Y-') + time.replace(u'月', '-').replace(u'日', '') + ':00'
                else:
                    weiboItem["PubTime"] = time
				

                # 获取转发工具
                if len(pubTime_tool) > 1:  # 有些微博不带发布平台
                    weiboItem["Tool"] = pubTime_tool[1]
                else:
                    weiboItem["Tool"] = None

                # 获取赞数目
                likeNumRe = ur'赞\[(\d+)\]'
                likeNum = re.search(likeNumRe, weibo.text)
                weiboItem["LikeNum"] = int(likeNum.group(1))

                # 获取转发数目
                transferNumRe = ur'转发\[(\d+)\]'
                transferNum = re.search(transferNumRe, weibo.text)
                weiboItem["TransferNum"] = int(transferNum.group(1))

                # 获取评论数目
                commentNumRe = ur'评论\[(\d+)\]'
                commentNum = re.search(commentNumRe, weibo.text)
                weiboItem["CommentNum"] = int(commentNum.group(1))

                yield weiboItem

        pagelist = body.find(id='pagelist')
        if pagelist:
            a = pagelist.find('a')
            href = a.attrs["href"]
            if href:
                yield Request(self.host + href, meta={"keyword": response.meta["keyword"]}, callback=self.parseSearch)
