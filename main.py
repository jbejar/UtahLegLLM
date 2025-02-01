import os
from dotenv import load_dotenv
from scraper.spider import WebsiteSpider
from openai_processor.processor import OpenAIProcessor
from scrapy.crawler import CrawlerProcess

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize the crawler process
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    # Run the spider
    process.crawl(WebsiteSpider)
    process.start()
    
    # Process data with OpenAI
    openai_processor = OpenAIProcessor()
    openai_processor.process_data()

if __name__ == "__main__":
    main()