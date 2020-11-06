# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
# import MySQLdb
# from scrapy.exceptions import NotConfigured
#
#
# class PlanetminecraftPipeline:
#
#     def __init__(self, db, user, passwd, host):
#         self.db = db
#         self.user = user
#         self.passwd = passwd
#         self.host = host
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         db_settings = crawler.settings.getdict("DB_SETTINGS")
#         if not db_settings:
#             raise NotConfigured
#         db = db_settings['db']
#         user = db_settings['user']
#         passwd = db_settings['passwd']
#         host = db_settings['host']
#         return cls(db, user, passwd, host)
#
#     def open_spider(self, spider):
#         self.conn = MySQLdb.connect(db=self.db,
#                                user=self.user, passwd=self.passwd,
#                                host=self.host,
#                                charset='utf8', use_unicode=True)
#         self.cursor = self.conn.cursor()
#
#     def process_item(self, item, spider):
#         sql = "INSERT INTO table (field1, field2, field3) VALUES (%s, %s, %s)"
#         self.cursor.execute(sql,
#                             (
#                                 item.get("field1"),
#                                 item.get("field2"),
#                                 item.get("field3"),
#                             )
#                             )
#         self.conn.commit()
#         return item
#
#
#     def close_spider(self, spider):
#         self.conn.close()
#
#
# class GCSFilesStoreJSON(GCSFilesStore):
#     CREDENTIALS = {
#         "type": "service_account",
#         "project_id": "COPY FROM CREDENTIALS FILE",
#         "private_key_id": "COPY FROM CREDENTIALS FILE",
#         "private_key": "COPY FROM CREDENTIALS FILE",
#         "client_email": "COPY FROM CREDENTIALS FILE",
#         "client_id": "COPY FROM CREDENTIALS FILE",
#         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#         "token_uri": "https://accounts.google.com/o/oauth2/token",
#         "auth_provider_x509_cert_url":
#            "https://www.googleapis.com/oauth2/v1/certs",
#        "client_x509_cert_url": "COPY FROM CREDENTIALS FILE"
#     }
# def __init__(self, uri):
#   from google.cloud import storage
#   client =
#       storage.Client.from_service_account_info(self.CREDENTIALS)
#   bucket, prefix = uri[5:].split('/', 1)
#   self.bucket = client.bucket(bucket)
#   self.prefix = prefix
# class GCSFilePipeline(FilesPipeline):
#     def __init__(self, store_uri, download_func=None, settings=None):
#         super(GCSFilePipeline, self).__init__(store_uri,download_func,settings)


class PlanetminecraftPipeline:
    def process_item(self, item, spider):
        return item
