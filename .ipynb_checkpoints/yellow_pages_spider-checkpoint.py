%%writefile yellow_pages_spider.py
import scrapy
import os

class YellowPagesSpider(scrapy.Spider):
    name = 'yellowpages'
    start_urls = []

    def __init__(self, cities=None, *args, **kwargs):
        super(YellowPagesSpider, self).__init__(*args, **kwargs)
        if cities:
            for city in cities:
                city_url = f"https://www.yellowpages.com/search?search_terms=all&geo_location_terms={city.replace(' ', '%20')},IL"
                self.start_urls.append(city_url)
        else:
            self.start_urls = ['https://www.yellowpages.com/search?search_terms=all&geo_location_terms=Marion,IL']

    def parse(self, response):
        city = response.url.split('geo_location_terms=')[1].split(',IL')[0].replace('%20', '_')
        filename = f"{city}_IL_businesses.csv"
        self.custom_settings = {
            'FEED_URI': filename,
            'FEED_FORMAT': 'csv'
        }

        for business in response.css('div.v-card'):
            yield {
                'name': business.css('a.business-name span::text').get(default=''),
                'address': business.css('div.info-section div.street-address::text').get(default=''),
                'phone': business.css('div.info-section div.phones::text').get(default=''),
                'category': business.css('div.info div.categories a::text').get(default=''),
                'website': business.css('a.track-visit-website::attr(href)').get(default='')
            }

        next_page = response.css('a.next.ajax-page::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

# Step 2: Run the Scrapy Spider for Multiple Cities
cities = [
    'Carbondale', 'Mt. Vernon', 'Murphysboro', 'Harrisburg', 
    "O'Fallon", 'Herrin', 'Edwardsville', 'Nashville', 
    'Pinckneyville', 'West Frankfort', 'Metropolis'
]

# Write the cities to a file
with open('cities.txt', 'w') as f:
    for city in cities:
        f.write(f"{city}\n")
