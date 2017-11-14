# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item


class Question(Item):
    tags = Field()
    answers = Field()
    votes = Field()
    date = Field()
    link = Field()
