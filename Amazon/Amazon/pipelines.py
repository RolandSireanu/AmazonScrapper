# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3


class AmazonPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()
        pass

    def create_connection(self):
        self.conn = sqlite3.connect("amazon.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute(""" drop table if exists amazonBooks """)
        self.curr.execute(""" create table amazonBooks(title text , author text , image text , price text)""")

    def store_in_db(self , arg_item):
        #print(arg_item["product_name"])
        for idx , i in enumerate(arg_item["product_name"]):
            if("Hardcover" in arg_item["product_prices"][idx]):
                self.curr.execute(""" INSERT INTO amazonBooks values (?,?,?,?)""" , 
                (str(arg_item["product_name"][idx]) , 
                str(arg_item["product_author"][idx]) , 
                str(arg_item["product_imagelink"][idx]) , 
                arg_item["product_prices"][idx]["Hardcover"]))
            else:
                self.curr.execute(""" INSERT INTO amazonBooks values (?,?,?,?)""" , 
                (str(arg_item["product_name"][idx]) , 
                str(arg_item["product_author"][idx]) , 
                str(arg_item["product_imagelink"][idx]) , 
                "Not available"))

        self.conn.commit()

    def process_item(self, item, spider):

        self.store_in_db(item)

        return item
