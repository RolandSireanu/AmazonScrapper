# -*- coding: utf-8 -*-
import scrapy
from ..items import AmazonItem
from time import sleep
from bs4 import BeautifulSoup
import bs4
class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    allowed_domains = ['amazon.com']
    start_urls = ["https://www.amazon.com/Books-Last-30-days/s?i=stripbooks&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&page=3&qid=1583090067&ref=sr_pg_2"]
    #start_urls = ["file:///home/sireanuroland/Works/amazonScraping/Amazon/source_page1.html"]
    #start_urls = ["file:///home/sireanuroland/Works/amazonScraping/Amazon/simple.html"]


    custom_settings = {
        'ROBOTSTXT_OBEY': 'True'
    }

    def debugSaveResponse(self , response):        
        f = open("index.html" , "w")
        author = open("author.html" , "w")
        f.write(response.text)
        f.close()        


    def getProductAuthor(self , response):

        listOfAuthors : list = []

        product_author = response.css(".sg-col-12-of-28 .a-color-secondary").extract()

        for prodAuthorTag in product_author:
            
            authorsName : str = ""

            bsData = BeautifulSoup(prodAuthorTag , features="html.parser")            
            link = bsData.find("a" , class_="a-size-base a-link-normal")

            #Check if the a tag was found
            if(link != None):                
                authorsName = authorsName + " " + link.get_text().strip()


            authorList = bsData.find_all(lambda tag: tag.name == 'span' and 
                                   tag.get('class') == ['a-size-base'])
                                
            for a in authorList:
                if a != None:
                    if a.get_text().strip() != "by":                        
                        authorsName = authorsName + " " + a.get_text().strip()

            if(authorsName != ""):
                listOfAuthors.append(authorsName)
            
        return listOfAuthors;

    def getProductPrices(self , response):

        listOfPrices : list = []
        product_price = response.css(".sg-col-20-of-28 .sg-col-4-of-32 .sg-col-inner").extract()

        for priceElement in product_price:
            tempDict : dict = {}
            bsObject = BeautifulSoup(priceElement , features="html.parser")
            booksFormat = bsObject.findAll("a" , class_="a-size-base a-link-normal a-text-bold")
            for bookF in booksFormat :                
                #print(tt.get_text().strip())
                typeOfBook = bookF.get_text().strip();
                priceOfThisTypeOfBook = 0
                temp = bookF.parent.next_sibling
                
                if(isinstance(temp , bs4.element.Tag)):                                    
                    priceOfThisTypeOfBook = temp.find("span" , {"class": "a-offscreen"}).get_text().strip()
                    #print(temp.find("span" , {"class": "a-offscreen"}).get_text())
                elif (isinstance(temp ,  bs4.element.NavigableString)):
                    priceOfThisTypeOfBook = "Unknown"                    
                else:
                    pass
                
                tempDict[typeOfBook] = priceOfThisTypeOfBook;
            listOfPrices.append(tempDict);

        return listOfPrices


    #Spider will gather all the books together with Name , Author , Img link and price 
    #In Pipeline will be stored in sqlite database
    def parse(self, response):        
    
        container = AmazonItem()        
        product_name = response.css(".a-color-base.a-text-normal::text").extract()            
        product_img = response.css("img.s-image::attr(src)").extract()
        
        
        listOfAuthors = self.getProductAuthor(response)
        listOfPrices = self.getProductPrices(response)            

        container['product_name'] = product_name
        container['product_author'] = listOfAuthors
        container['product_imagelink'] = product_img        
        container["product_prices"] = listOfPrices

        print("--------------------------")
        print(len(product_name))
        print(len(listOfAuthors))
        print(len(product_img))
        print(len(listOfPrices))

        yield container