# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import doubanSpider.settings as setting

class DoubanspiderPipeline(object):

    def __init__(self):
        self.connect = pymysql.connect(
            host = setting.MYSQL_HOST,
            db = setting.MYSQL_DBNAME,
            user = setting.MYSQL_USRE,
            passwd = setting.MYSQL_PASSWD,
            charset = 'utf8',
            use_unicode = True,
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """
                    insert into doubantop250(title,movieinfo,star,quote)
                    value (%s,%s,%s,%s)
                """,
                (
                    item["title"],
                    item["movieInfo"],
                    item["star"],
                    item["quote"]
                )
            )
            self.connect.commit()

        except Exception as e:
            print("重复插入了 ==> 错误信息为：" + str(e))
        return item
