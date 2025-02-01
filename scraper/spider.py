import scrapy
import json

class WebsiteSpider(scrapy.Spider):
    name = 'website_spider'
    # Add your start URLs here
    start_urls = ['https://example.com']
    
    def parse(self, response):
        """
        Parse the webpage and extract relevant data.
        Modify this method according to your specific scraping needs.
        """
        data = {
            'title': response.css('h1::text').get(),
            'content': response.css('p::text').getall(),
        }
        
        # Save the scraped data to a JSON file
        with open('scraped_data.json', 'w') as f:
            json.dump(data, f, indent=4)
            
        yield data