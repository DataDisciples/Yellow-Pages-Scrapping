import scrapy

class YellowPagesSpider(scrapy.Spider):
    name = 'yellow_pages'
    allowed_domains = ['yellowpages.com']

    def start_requests(self):
        cities = [
            'Sesser', 'Royalton', 'Cairo', 'Vienna', 'Zeigler',
            'Stonefort', 'Thompsonville', 'Johnston City', 'Eldorado',
            'Benton', 'Galatia', 'Mulkeytown', 'Ozark', 'Akin', 'Christopher'
        ]
        for city in cities:
            url = f"https://www.yellowpages.com/search?search_terms=all&geo_location_terms={city},IL"
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for business in response.css('div.result'):
            yield {
                'name': business.css('a.business-name span::text').get(),
                'address': business.css('div.street-address::text').get(),
                'phone': business.css('div.phones.phone.primary::text').get(),
                'category': business.css('div.categories a::text').get(),
                'website': business.css('a.track-visit-website::attr(href)').get(default=''),
            }
        
        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
