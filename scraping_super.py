from datetime import date
import pandas as pd
import re
import scrapy
from scrapy.crawler import CrawlerProcess
import time

LIST_DIR = "list.csv"
SNAPSHOT_DIR = "snapshots"

date = str(date.today())
df = pd.read_csv(LIST_DIR)
links_coto =  list(df.link_coto)
links_disco = list(df.link_disco)
price_snapshot_coto = []
price_snapshot_disco = []


class Coto(scrapy.Spider):
    name = 'coto'

    def start_requests(self):
        urls = links_coto
        for url in urls:
            if 'coto' in url:
                yield scrapy.Request(url=url, callback=self.parse)
            else: pass

    def parse(self, response):
        cada_link = response.request.url
        price_step1 = response.css('.atg_store_newPrice').get()
        price_step2 = re.findall(r'\$(.*),', price_step1) #sin centavos, solo enteros
        price = ''.join(price_step2) #Perfecto!
        item_name = df.loc[df["link_coto"] == cada_link, "item"].iloc[0]
        item_dict = {'item': item_name, 'price': price, 'date': date, 'retailer': 'COTO'}
        price_snapshot_coto.append(item_dict)
        time.sleep(3)


class Disco(scrapy.Spider):
    name = 'disco'

    def start_requests(self):
        urls = links_disco
        for url in urls:
            if 'disco' in url:
                yield scrapy.Request(url=url, callback=self.parse)
            else: pass

    def parse(self, response):
        cada_link = response.request.url
        meta_tags = response.css('meta').getall()
        for i in meta_tags:
            if "product:price:amount" in i:
                price= re.findall(r'content=\"([0-9]*)', i)
                price = ''.join(price)
        item_name = df.loc[df["link_disco"] == cada_link, "item"].iloc[0]
        item_dict = {'item': item_name, 'price': price, 'date': date, 'retailer': 'DISCO'}
        price_snapshot_disco.append(item_dict)
        time.sleep(3)


process = CrawlerProcess()
process.crawl(Coto)
process.crawl(Disco)
process.start()
price_snapshot = price_snapshot_coto + price_snapshot_disco
snapshot_df = pd.DataFrame(price_snapshot)


try:
    with open(f'{SNAPSHOT_DIR}/prices_{date}.csv', 'a') as f:
        snapshot_df.to_csv(f, index=False, header=f.tell()==0)
except:
    print("===ERROR===")
