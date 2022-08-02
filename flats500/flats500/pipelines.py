# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class FlatsPipeline:
    def __init__(self):
        self.conn = psycopg2.connect(dbname="postgres_database", user="postgres", password="heslo123", host="postgres_db", port="5432")
        self.cursor = self.conn.cursor()
        self.cursor.execute("DROP TABLE IF EXISTS flats")
        self.cursor.execute("CREATE TABLE flats (id serial PRIMARY KEY, name varchar, location varchar, image_link varchar);")

    def process_item(self, item, spider):
        flat_name = item['name']
        flat_location = item['location']
        flat_image = item['image']
        self.cursor.execute("INSERT INTO flats (name, location, image_link) VALUES (%s, %s, %s)", (flat_name, flat_location, flat_image))

        return item
    def close_spider(self, spider):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
