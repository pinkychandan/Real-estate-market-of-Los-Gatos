from scrapy import Spider, Request
from redfin.items import RedfinItem
import re

class RedfinSpider(Spider):
    name = 'redfin_spider'
    allowed_urls = ['https://www.redfin.com']
    start_urls = ['https://www.redfin.com/city/11234/CA/Los-Gatos/filter/include=sold-3yr']
    

    def parse(self, response):
        # Find the total number of pages in the result so that we can decide how many urls to scrape next
        #we have per page and total products
        num_prods = (response.xpath('//div[@class="homes summary"]/text()').extract_first())
        per_page,total_prod = map(int,re.findall('(\d+) of (\d+)',num_prods)[0])


        if total_prod%per_page==0:
            total_pages=total_prod//per_page
        else:
            total_pages=total_prod//per_page + 1
        #print(total_pages)
        #print('='*50)

        ###making results url list#
        url_list = ['https://www.redfin.com/city/11234/CA/Los-Gatos/filter/include=sold-3yr/page-{}'.format(i+1) for i in range(total_pages)]

        #callback is the name of the function to whom we are sending the url to
        for url in url_list:
            yield Request(url=url, callback=self.parse_result_page)


    def parse_result_page(self,response):
        # this fucntion parses the search result page.
        # We are looking for home detail page url.
        listing_urls = list(set(response.xpath('//div[@class="homecards"]//a/@href').extract()))
        listing_urls = ['https://www.redfin.com' + s for s in listing_urls]
        #First checkpoint gives the number of listings per page
        #print('='*50)
        #print(len(listing_urls))
        #print(listing_urls)
        #print('='*50)

        for url in listing_urls:
            yield Request(url=url, callback=self.parse_detail_page)#each home listing image on a page



    def parse_detail_page(self, response):
        # This fucntion parses each home listing to get items.


        street=response.xpath('//span[@class="street-address"]/text()').extract_first()
        city=response.xpath('//span[@class="locality"]/text()').extract_first()
        
       
        Soldprice = response.xpath('//div[@class="info-block price"]/div/text()').extract_first()
        #Soldprice[Soldprice.find(">")+1:Soldprice.find("</div>")] don't use
        Soldprice = Soldprice.strip("$")
        Soldprice = Soldprice.replace(",","")
        Soldprice = float(Soldprice)

        Bedrooms = response.xpath('//div[@data-rf-test-id="abp-beds"]/div/text()').extract_first()
        #Bedrooms[Bedrooms.find(">")+1:Bedrooms.find("</div>")] dont use
        Bedrooms = float(Bedrooms)

        Bathroom = response.xpath('//div[@data-rf-test-id="abp-baths"]/div/text()').extract_first()
        #Bathroom[Bathroom.find(">")+1:Bathroom.find("</div>")] don't use
        Bathroom = float(Bathroom)

        SqFeet = response.xpath('//div[@class="info-block sqft"]/span').extract_first()
        SqFeet = SqFeet[SqFeet.find("\">")+2:SqFeet.find("</span>")]
        SqFeet = SqFeet.replace(",","")
        SqFeet = float(SqFeet)


        Redfinestimate = response.xpath('//div[@data-rf-test-id="avm-price"]/div/text()').extract_first()
        Redfinestimate = Redfinestimate.strip("$")
        Redfinestimate = Redfinestimate.replace(",","")
        Redfinestimate = float(Redfinestimate)

        Solddate = response.xpath('//span[@class="HomeSash"]/text()').extract_first()
        Solddate = Solddate.replace("SOLD BY REDFIN ","")

        # Initialize a new Redfin Item instance for each sold home.
        
        item = RedfinItem()
        item['Streetname']= street
        item['City']= city
        item['Bedrooms']= Bedrooms
        item['Bathrooms']= Bathroom
        item['SqFeet']= SqFeet
        item['Soldprice']= Soldprice
        #item['Listedprice']=
        item['Currentestimate']=  Redfinestimate     
        #item['Listdate']=
        item['Solddate']= Solddate
        #item['Pricecut']=





        yield item


