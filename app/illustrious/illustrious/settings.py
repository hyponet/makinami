# -*- coding: utf-8 -*-

# Scrapy settings for illustrious project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'illustrious'

SPIDER_MODULES = ['illustrious.spiders']
NEWSPIDER_MODULE = 'illustrious.spiders'

MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DATABASE = 'makinami'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'illustrious (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'illustrious.pipelines.MongoPipeline': 300,
}
