import openpyxl
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface


class MoviePipeline:

    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.title = "Top250"
        self.ws.append(("电影名称", "主演", "详情页", "简介"))

    def close_spider(self, spider):
        self.wb.save("豆瓣Top250.xlsx")
        # self.wb.close()

    def process_item(self, item, spider):
        name = item.get("name", "")
        author = item.get("author", "")
        href = item.get("href", "")
        brief_introduction = item.get("brief_introduction", "")
        self.ws.append((name, author, href, brief_introduction))
        return item
