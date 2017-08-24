import scrapy
#from bs4 import BeautifulSoup
from datetime import datetime, timedelta
#from json import dumps
import os
from lkmlspider.items import LkmlEmailItem
#import requests
#import urlparse



class LkmlSpider(scrapy.Spider):
    name = "lkml"
    # urls 1996 - present (one in 1919 due to some error) */
    def start_requests(self):
        # write generator
        while True:
            #archive_dir = "archive/"
            start_datetime = datetime(year=1996, month=1, day=1, hour=0, minute=0, second=0)
            today_datetime = datetime.now()
            #lkml_archive_day_url = base_url.format(year=current_datetime.year, month=current_datetime.month, day=current_datetime.day)
            #day_http_request = requests.get(lkml_archive_day_url)
            base_url = "http://lkml.org/lkml/"
            urls = []
            for date in range ((today_datetime - start_datetime).days + 1):
                scrape_datetime = start_datetime + timedelta(days=date)
                self.log("Appending url {}".format(scrape_datetime.strftime("%Y-%m-%d")))
                urls.append(base_url + str(scrape_datetime.year) + "/" + str(scrape_datetime.month) + "/" + str(scrape_datetime.day))
            #"https://lkml.org/lkml/2004/7/7/2"             ]
            for url in urls:
                self.log("Scraping %s" % url)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        archive_dir = "archive/"
        url_list = response.url.split("/")
        day = url_list[-1]
        month = url_list[-2]
        year = url_list[-3]
        #returns all hrefs that contain lkml which should be all emails for a given date - also still catches some forbidden pages like lkml/bounce or similar
        #xpath_query = "//a[contains(@href, 'lkml')]/@href"
        r = response.xpath("//a[contains(@href, 'lkml/')]/@href").extract()
        # delete link to year, month, day and last100 - could be excluded with fancier xpath I guess
        del r[0:4]
        for link in r:
            if link is not None:
                yield response.follow(link, callback=self.parse_email_page)
        #this would be for re
        #new_request = Request(link, callback=self.parse_email_page)

        self.log('Parsed %s %s %s' % (year, month, day))
        #if "{year}/{month}/{day}/".format(year=current_datetime.year, month=current_datetime.month, day=current_datetime.day) in str(tag_href) and tag_href not in lkml_day_message_set:

    def parse_email_page(self, response):
        mail_subject = response.xpath("//td[.='Subject']/following-sibling::td/text()").extract()
        mail_author = response.xpath("//td[.='From']/following-sibling::td/text()").extract()
        mail_date = response.xpath("//td[.='Date']/following-sibling::td/text()").extract()
        mail_content = response.xpath("//pre[contains(@itemprop, 'articleBody')]/text()").extract() #somehow in json pre/articleBody is still present???
        url_list = response.url.split("/")
        mail_number = url_list[-1]
        mail_day = url_list[-2]
        mail_month = url_list[-3]
        mail_year = url_list[-4]
        mailitem = LkmlEmailItem(subject=mail_subject, sender=mail_author, date=mail_date, body=mail_content, year=mail_year, month=mail_month, day=mail_day, number=mail_number)
        return mailitem
            



"""
from scrapy.loader import ItemLoader
from myproject.items import Product

def parse(self, response):
    l = ItemLoader(item=Product(), response=response)
    l.add_xpath('name', '//div[@class="product_name"]')
    l.add_xpath('name', '//div[@class="product_title"]')
    l.add_xpath('price', '//p[@id="price"]')
    l.add_css('stock', 'p#stock]')
    l.add_value('last_updated', 'today') # you can also use literal values
    return l.load_item()
    """

"""
  
                try:
                    message_subject = message_soup.findAll("td", text="Subject")[0].findNext("td").text
                    message_date = message_soup.findAll("td", text="Date")[0].findNext("td").text
                    message_sender = message_soup.findAll("td", text="From")[0].findNext("td").text
                    message_body_element = message_soup.findAll("pre", attrs = {'itemprop': 'articleBody'})[0]
                    message_body = ""
                    for element in message_body_element.children:
                        line_content = str(element)
                        if "<br/>" == line_content:
                            message_body += "\n"
                        else:
                            message_body += line_content
                except:
                    continue
                data = {
                    'subject': message_subject,
                    'date': message_date,
                    'sender': message_sender,
                    'body': message_body
                        }
                filename = tag_href[1:].replace("/",".") + ".email.json"
                fh = open(archive_dir + filename, "w")
                fh.write(dumps(data))
                fh.close() """

#if __name__ == "__main__":
#    scrape()
