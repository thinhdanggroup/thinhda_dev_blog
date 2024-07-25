import scrapy
import scrapy.crawler

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://sdt.wiki/thong-tin-so-dien-thoai-0903333505']  # Replace this with the URL of the website you want to scrape

    def parse(self, response):
        # Extract data using XPath
        panel_body = response.xpath('/html/body/main/div/div[2]/div[2]')
        print(panel_body)
        
        # Extracting individual pieces of information
        updated_date = panel_body.xpath('ul/li[1]/text()').get().strip()
        views = panel_body.xpath('ul/li[2]/text()').get().strip()
        search_views = panel_body.xpath('ul/li[2]/ul/li/text()').get().strip()
        total_ratings = panel_body.xpath('ul/li[3]/span/text()').get().strip()
        positive_ratings = panel_body.xpath('ul/ul/li[1]/span/text()').get()
        if positive_ratings:
            positive_ratings = positive_ratings.strip()
        
        negative_ratings = panel_body.xpath('ul/ul/li[2]/span/text()').get()
        if negative_ratings:
            negative_ratings = negative_ratings.strip()
            
        uncertain_ratings = panel_body.xpath('ul/ul/li[3]/span/text()').get()
        if uncertain_ratings:
            uncertain_ratings = uncertain_ratings.strip()
            
        network = panel_body.xpath('ul/li[4]/text()').get().strip()
        result = panel_body.xpath('ul/li[5]/span/span/text()').get().strip()
        
        comment_items = response.xpath('/html/body/main/div/div[3]/div[2]')
        
        comments = []
        
        # Iterate over each comment item and extract comment text and date
        i = 1
        while True:
            comment_text = comment_items.xpath(f'div[{i}]/text()').get()
            print(comment_text)
            if not comment_text:
                break
            
            comments.append({
                'comment_text': comment_text,
            }) 
            i+=1

        yield {
            'updated_date': updated_date,
            'views': views,
            'search_views': search_views,
            'total_ratings': total_ratings,
            'positive_ratings': positive_ratings,
            'negative_ratings': negative_ratings,
            'uncertain_ratings': uncertain_ratings,
            'network': network,
            'result': result,
            "comments": comments,
        }

if __name__ == "__main__":
    process = scrapy.crawler.CrawlerProcess(settings={
        "FEEDS": {
            "output.json": {"format": "json"},
        },
    })

    process.crawl(MySpider)
    process.start()