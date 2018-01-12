# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class FinishedIDItem(Item):
    _id = Field()


class InfoItem(Item):
    _id = Field()  # 用户ID
    NickName = Field()  # 昵称
    Gender = Field()  # 性别
    Province = Field()  # 所在省
    City = Field()  # 所在城市
    Signature = Field()  # 个性签名
    Birthday = Field()  # 生日
    WeiboNum = Field()  # 微博数
    FollowNum = Field()  # 关注数
    FanNum = Field()  # 粉丝数
    SexOrientation = Field()  # 性取向
    Marriage = Field()  # 婚姻状况


class WeiboItem(Item):
    _id = Field()  # 微博ID
    UserID = Field()  # 用户ID
    Content = Field()  # 微博内容
    PubTime = Field()  # 发表时间
    Tool = Field()  # 发表工具/平台
    LikeNum = Field()  # 点赞数
    CommentNum = Field()  # 评论数
    TransferNum = Field()  # 转载数


class SearchWeiboItem(Item):
    _id = Field()
    UserName = Field()
    Keyword = Field()
    Content = Field()  # 微博内容
    PubTime = Field()  # 发表时间
    Tool = Field()  # 发表工具/平台
    LikeNum = Field()  # 点赞数
    CommentNum = Field()  # 评论数
    TransferNum = Field()  # 转载数


class UsersRelationItem(Item):
    FanID = Field()
    FollowID = Field()


class FollowsItem(Item):
    """ 关注人列表 """
    _id = Field()  # 用户ID
    follows = Field()  # 关注


class FansItem(Item):
    """ 粉丝列表 """
    _id = Field()  # 用户ID
    fans = Field()  # 粉丝