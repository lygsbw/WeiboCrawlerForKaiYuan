# coding: utf-8
import re

from scrapy.spiders import BaseSpider
from scrapy.http import Request
from WeiboCrawler.items import InfoItem, WeiboItem, UsersRelationItem, FinishedIDItem
from scrapy.selector import Selector
from bs4 import BeautifulSoup
import datetime
from WeiboCrawler.getUnfinishedID import getUnfinishedID

class Spider(BaseSpider):
    name = "weiboCrawler"
    host = "http://weibo.cn"
    """
    # ID分别为：人民日报，央视新闻，每日经济新闻，21世纪经济报道，
    #           新浪娱乐，微博新鲜事， CCTV5， 新浪体育
    start_urls = [
        '2803301701', '2656274875', '1649173367', '1651428902',
        '1642591402', '2431328567', '2993049293', '1638781994',
    ]
    unfinishedID = set(start_urls)
    """
    unfinishedID = set(getUnfinishedID())   # return 100000 ID
    finishedID = set()
    # logging.getLogger("requests").setLevel(logging.WARNING)  # 将requests的日志级别设成WARNING

    def start_requests(self):
        """
        程序入口
        """
        account_num = len(self.unfinishedID)
        print 'get %d accounts' % account_num
        count = 0

        while count != account_num:

            # 从未爬取的ID中取一个
            ID = self.unfinishedID.pop()


            # 初步获取微博数，关注数，粉丝数等信息
            # urlInfo0 = "http://weibo.cn/attgroup/opening?uid=%s" % ID
            # yield Request(urlInfo0, meta={"ID": ID}, callback=self.parseInfo0)

            # 爬取微博数据
            urlWeibo = "http://weibo.cn/%s/profile?filter=1&page=1" % ID
            yield Request(urlWeibo, meta={"ID": ID}, callback=self.parseWeibo)

            # 爬取关注人列表
            # urlFollow = "http://weibo.cn/%s/follow" % ID
            # yield Request(url=urlFollow, meta={"ID": ID, "Page": "Follow"}, callback=self.parseRelation)

            # 爬取粉丝列表
            ### 注释原因是数据太多了，没多大意义而又影响爬取效率
            # urlFan = "http://weibo.cn/%s/fans" % ID
            #　yield Request(url=urlFan, meta={"ID": ID, "Page": "Fan"}, callback=self.parseRelation)

            # 把ID加入finishedID里
            # 这里注意对该ID的爬取工作并非已经完成，因为对于每个url，scrapy会新建一个线程去爬取
            self.finishedID.add(ID)
            count += 1

    def parseInfo0(self, response):
        """
        初步获取粉丝数，关注数，微博数
        """
        infoItem = InfoItem()
        selector = Selector(response=response)
        Weibo_Follow_Fan = selector.xpath(
            'body/div[@class="u"]/div[@class="tip2"]').extract_first()
        if Weibo_Follow_Fan:
            # 微博数
            weiboNum = re.findall(u'微博\[(\d+)\]', Weibo_Follow_Fan)
            infoItem["WeiboNum"] = int(weiboNum[0]) if weiboNum else -1

            # 关注数
            followNum = re.findall(u'关注\[(\d+)\]', Weibo_Follow_Fan)
            infoItem["FollowNum"] = int(followNum[0]) if followNum else -1

            # 粉丝数
            fanNum = re.findall(u'粉丝\[(\d+)\]', Weibo_Follow_Fan)
            infoItem["FanNum"] = int(fanNum[0]) if fanNum else -1

            infoItem["_id"] = response.meta["ID"]

            urlInfo1 = 'http://weibo.cn/%s/info' % infoItem["_id"]

            yield Request(url=urlInfo1, meta={"item": infoItem}, callback=self.parseInfo1)

    def parseInfo1(self, response):
        """
        获取更多的用户信息，如性别，年龄等
        """
        selector = Selector(response=response)
        # 获取源码中div为c类下的所有text(),并用;分隔开
        info = ";".join(selector.xpath(
            'body/div[@class="c"]/text()').extract())

        infoItem = response.meta["item"]

        nickname = re.findall(u'昵称:(.*?);', info)  # 昵称
        infoItem["NickName"] = nickname[0] if nickname else None

        gender = re.findall(u'性别:(.*?);', info)  # 性别
        if gender:
            if gender == '男':
                infoItem["Gender"] = 1
            elif gender == '女':
                infoItem["Gender"] = 0
            else:
                infoItem["Gender"] = -1
        else:
            infoItem["Gender"] = None

        place = re.findall(u'地区:(.*?);', info)  # 地区（包括省份和城市）
        if place:
            place = place[0].split(" ")
            infoItem["Province"] = place[0]
            infoItem["City"] = place[1] if len(place) > 1 else None
        else:
            infoItem["Province"] = None
            infoItem["City"] = None

        signature = re.findall(u'个性签名:(.*?);', info)  # 个性签名
        infoItem["Signature"] = signature[0] if signature else None

        birthday = re.findall(u'生日:(.*?);', info)  # 生日
        infoItem["Birthday"] = birthday[0] if birthday else None

        sexorientation = re.findall(u'性取向:(.*?);', info)  # 性取向
        infoItem["SexOrientation"] = sexorientation[0] if sexorientation else None

        marriage = re.findall(u'感情状况:(.*?);', info)  # 婚姻状况
        infoItem["Marriage"] = marriage[0] if marriage else None

        yield infoItem

    def parseWeibo(self, response):
        """
        获取微博信息
        :param response: 从服务端发来的response
        :return: 一条完整的微博信息
        """
        soup = BeautifulSoup(response.text, "lxml")
        body = soup.body
        weiboList = body.find_all(attrs={'class': 'c'})
        flag = True
        for weibo in weiboList:

            weiboItem = WeiboItem()

            # 如果这个div中包含原文内容的话
            if weibo.find(attrs={'class': 'ctt'}):

                weiboItem["_id"] = weibo.attrs["id"]

                weiboItem["UserID"] = response.meta["ID"]

                # 获取内容
                weiboItem["Content"] = weibo.find(
                    attrs={'class': 'ctt'}).text.strip().replace('\n', '')
                # print weiboItem["Content"].encode('gb18030')

                # 获取转发时间
                pubTime_tool = weibo.find(attrs={'class': 'ct'})
                pubTime_tool = pubTime_tool.text.strip().replace('\n', '').split(u'来自')
                time = pubTime_tool[0].strip()
                now = datetime.datetime.now()
                if time[:2] == u'今天':
                    weiboItem["PubTime"] = now.strftime('%Y-%m-%d ') + time[2:]
                elif time[-3:] == u'分钟前':
                    minutes = datetime.timedelta(minutes=int(time[:-3]))
                    weiboItem["PubTime"] = (now - minutes).strftime('%Y-%m-%d %H:%M:%S')
                elif u'月' in time and u'日' in time:
                    weiboItem["PubTime"] = now.strftime('%Y-')+time.replace(u'月', '-').replace(u'日', '')+':00'
                else:
                    weiboItem["PubTime"] = time

                """
                抓取17年5月,6月的微博
                """
                if weiboItem["PubTime"][:7] != '2017-05' and weiboItem["PubTime"][:7] != '2017-06':
                    flag = False
                    break


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

        if flag:
            pagelist = body.find(id='pagelist')
            if pagelist:
                a = pagelist.find('a')
                href = a.attrs["href"]
                if href:
                    yield Request(self.host + href, meta={"ID": response.meta["ID"]}, callback=self.parseWeibo)
        else:
            user = FinishedIDItem()
            user["_id"] = response.meta["ID"]
            yield user

    def parseRelation(self, response):
        """
        爬取关注列表或粉丝列表
        :param response: 从服务端发来的response
        :return: RelationItem或新请求(爬取下一页)
        """
        selector = Selector(response=response)
        usersRelationItem = UsersRelationItem()
        users = selector.xpath(
            u'body//table/tr/td/a[text()="关注她" or text()="关注他"]/@href').extract()
        for user in users:
            userID = re.findall('uid=(\d+)', user)
            if userID:
                if response.meta["Page"] == "Follow":
                    usersRelationItem["FanID"] = response.meta["ID"]
                    usersRelationItem["FollowID"] = userID[0]
                else:
                    usersRelationItem["FanID"] = userID[0]
                    usersRelationItem["FollowID"] = response.meta["ID"]
                if userID[0] not in self.finishedID:
                    self.unfinishedID.add(userID[0])
                    # print '未爬取的ID个数为', self.unfinishedID.__len__()
                yield usersRelationItem
        nextPageURL = selector.xpath(
            u'body//div[@class="pa" and @id="pagelist"]/form/div/a[text()="下页"]/@href').extract()
        if nextPageURL:
            yield Request(self.host + nextPageURL[0], meta={"ID": response.meta["ID"], "Page": response.meta["Page"]}, callback=self.parseRelation)

