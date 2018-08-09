'''
python3
scrapy is required
'''

from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import json


from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

result=[]

class bondS(scrapy.Spider):
    name = "bondrate"
    start_urls = [
        'https://cn.investing.com/rates-bonds/china-10-year-bond-yield',]

    def parse(self, response):
        bond={"title":response.css("span#last_last::text").extract_first()+'%',"subtitle":"十年期国债收益率",'arg':self.start_urls[0]}
        result.append(bond)

class bitS(scrapy.Spider):
    name='bitdollas'
    start_urls=[ 
        'https://cn.investing.com/crypto/bitcoin',
        ]
    def parse(self, response):
        #print(response.request.headers['User-Agent'])
        bit={"title":response.css("span#last_last::text").extract_first(),"subtitle":"比特币美元",'arg':self.start_urls[0]}
        result.append(bit)

class goldS(scrapy.Spider):
    name = "gold"
    start_urls = [
        'https://cn.investing.com/commodities/gold',
        ]

    def parse(self, response):
        bond={"title":response.css("span.arial_26::text").extract_first(),"subtitle":"黄金期货美元",'arg':self.start_urls[0]}
        result.append(bond)

class dollarS(scrapy.Spider):
    name = "dollar"
    start_urls = [
        'https://cn.investing.com/currencies/usd-cny',
    ]

    def parse(self, response):
        bond={"title":response.css("span.arial_26::text").extract_first(),"subtitle":"人民币美元汇率",'arg':self.start_urls[0]}
        result.append(bond)

class oilS(scrapy.Spider):
    name = "oil"
    start_urls = [
        'https://cn.investing.com/commodities/brent-oil',
    ]

    def parse(self, response):
        bond={"title":response.css("span.arial_26::text").extract_first(),"subtitle":"原油期货美元",'arg':self.start_urls[0]}
        result.append(bond)

# configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
# turn the debug log in terminal off/on

runner = CrawlerRunner(            {
                'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            })

runner.crawl(bondS)
runner.crawl(bitS)
runner.crawl(goldS)
runner.crawl(dollarS)
runner.crawl(oilS)
d=runner.join()

d.addBoth(lambda _: reactor.stop())

reactor.run() 

print(json.dumps({'items':result}))