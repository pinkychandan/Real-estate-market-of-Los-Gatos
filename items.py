# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RedfinItem(scrapy.Item):
    # define the fields for your item here like:
	Streetname = scrapy.Field()    
	City = scrapy.Field()
	Bedrooms = scrapy.Field()
	Bathrooms = scrapy.Field()
	SqFeet = scrapy.Field()
    #Listedprice = scrapy.Field()
	Soldprice = scrapy.Field()
	Currentestimate = scrapy.Field()    
    #Listdate = scrapy.Field()
	Solddate = scrapy.Field()
    #Pricecut = scrapy.Field()