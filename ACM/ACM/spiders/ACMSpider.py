import scrapy
from ACM.items  import AcmItem
from scrapy_splash import SplashRequest
from scrapy import Selector
from datetime import datetime
class ACMSpider(scrapy.Spider):
    name = 'acm'
    topic= "None"

    def __init__(self, keywords=None, topic=None, *args, **kwargs):
        super(ACMSpider , self).__init__(*args,**kwargs)
        self.start_urls = ['https://dl.acm.org/action/doSearch?AllField=%s'%keywords]
        self.topic = topic

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield SplashRequest(url,self.parse,headers=headers,args={'wait': 2})
            
    def parse(self,response):
       for article in response.css('a::attr(href)'):
            if '/doi/' in article.extract():
                yield SplashRequest('https://dl.acm.org' + article.extract(), self.parse_details, args={'wait': 2})

    def parse_details(self, response):
       items = AcmItem()
       title = response.css('h1.citation__title::text').extract_first()
       authors = response.css('span.auth-name').css('a::text').extract()
       date_pub = response.css('span.epub-section__date::text').extract()
       journal = response.css('p.publisher__name::text').extract_first()
       laboratoire = response.css('span.auth-institution::text').extract()
       if len(laboratoire) == 0:
            laboratoire = response.css('span.loa_author_inst').css('p::text').extract()
       items['title'] = title
       items['authors'] = authors
       items['journal'] = journal
       items['laboratoire'] = laboratoire
       items['date_pub'] = str(datetime.strptime(date_pub[0].strip(), '%B %Y').date())
       yield items 