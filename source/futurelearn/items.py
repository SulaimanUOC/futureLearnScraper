# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CourseItem(scrapy.Item):
    name = scrapy.Field()
    category = scrapy.Field()
    organization = scrapy.Field()
    score = scrapy.Field()
    reviews = scrapy.Field()
    duration = scrapy.Field()
    weekly_study = scrapy.Field()
    accreditation = scrapy.Field()
    subscription_type = scrapy.Field()
    subscription_price = scrapy.Field()

