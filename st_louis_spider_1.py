
import scrapy

class st_louis_spider_1(scrapy.Spider):
    name = 'st_louis_spider_1'
    start_urls = ['https://www.yellowpages.com/search?search_terms=all&geo_location_terms=Des Peres,MO', 'https://www.yellowpages.com/search?search_terms=all&geo_location_terms=Ellisville,MO', 'https://www.yellowpages.com/search?search_terms=all&geo_location_terms=Fenton,MO', 'https://www.yellowpages.com/search?search_terms=all&geo_location_terms=Florissant,MO', 'https://www.yellowpages.com/search?search_terms=all&geo_location_terms=Hazelwood,MO']

    def parse(self, response):
        for business in response.css('div.result'):
            yield {
                'name': business.css('a.business-name span::text').get(),
                'address': business.css('div.street-address::text').get(),
                'phone': business.css('div.phones.phone.primary::text').get(),
                'category': business.css('div.categories a::text').get(),
                'website': business.css('div.links a::attr(href)').get()
            }

        next_page = response.css('a.next.ajax-page::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
