# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from DBConfig.DBConfig import DBConfig
from items import InfoItem, WeiboItem, UsersRelationItem, SearchWeiboItem, FinishedIDItem
import MySQLdb
import sys


class WeiboCrawlerPipeline(object):

    def __init__(self):
        try:
            self.conn = MySQLdb.connect(
                host=DBConfig.host,
                port=DBConfig.port,
                user=DBConfig.user,
                passwd=DBConfig.passwd,
                db=DBConfig.db,
                charset=DBConfig.charset,
                use_unicode=DBConfig.use_unicode)
            self.cursor = self.conn.cursor()
        except MySQLdb.Error as e:
            print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
            print 'Failed to connect to database! Please check your config file and confirm your database is open'
            sys.exit(-1)

    def process_item(self, item, spider):

        if isinstance(item, InfoItem):
            try:
                self.cursor.execute(
                    ('replace into information(ID, NickName, Gender, Province, City, Signature, '
                     'Birthday, WeiboNum, FollowNum, FanNum, SexOrientation, Marriage)'
                     'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'),
                    (item["_id"],
                        item["NickName"],
                        item["Gender"],
                        item["Province"],
                        item["City"],
                        item["Signature"],
                        item["Birthday"],
                        item["WeiboNum"],
                        item["FollowNum"],
                        item["FanNum"],
                        item["SexOrientation"],
                        item["Marriage"]))
                self.conn.commit()
            except MySQLdb.Error as e:
                print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
                sys.exit(-1)

        elif isinstance(item, WeiboItem):
            try:
                self.cursor.execute(
                    ('replace into weibo(_id, UserID, Content, PubTime, Tool, LikeNum, CommentNum, TransferNum)'
                     'values(%s,%s,%s,%s,%s,%s,%s,%s)'),
                    (item["_id"],
                        item["UserID"],
                        item["Content"],
                        item["PubTime"],
                        item["Tool"],
                        item["LikeNum"],
                        item["CommentNum"],
                        item["TransferNum"]))
                self.conn.commit()
            except MySQLdb.Error as e:
                print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
                sys.exit(-1)

        elif isinstance(item, UsersRelationItem):
            try:
                self.cursor.execute(
                    ('replace into usersrelation(fanID, followID)'
                     'values(%s,%s)'),
                    (item["FanID"],
                        item["FollowID"]
                    )
                )
                self.conn.commit()
            except MySQLdb.Error as e:
                print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
                sys.exit(-1)

        elif isinstance(item, SearchWeiboItem):
            try:
                self.cursor.execute(
                    ('replace into searchweibo(_id, UserName, Content, PubTime, Tool, LikeNum, CommentNum, TransferNum, Keyword)'
                     'values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'),
                    (item["_id"],
                        item["UserName"],
                        item["Content"],
                        item["PubTime"],
                        item["Tool"],
                        item["LikeNum"],
                        item["CommentNum"],
                        item["TransferNum"],
                        item["Keyword"]))
                self.conn.commit()
            except MySQLdb.Error as e:
                print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
                sys.exit(-1)

        elif isinstance(item, FinishedIDItem):
            try:
                self.cursor.execute(
                    ('replace into finishedid(_id)'
                     'values(%s)'),
                    (item["_id"], ))
                self.conn.commit()
            except MySQLdb.Error as e:
                print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
                sys.exit(-1)

        return item
