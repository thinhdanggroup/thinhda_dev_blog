import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def main():
    md_generator = DefaultMarkdownGenerator(
    content_filter=PruningContentFilter(threshold=0.4, threshold_type="fixed")
)
    browser_conf = BrowserConfig(headless=True)  # or False to see the browser
    run_conf = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        markdown_generator=md_generator
    )
    async with AsyncWebCrawler(config=browser_conf) as crawler:
        result = await crawler.arun("https://medium.com/gitconnected/the-5-paid-subscriptions-i-actually-use-in-2025-as-a-staff-software-engineer-98033c94566e", config=run_conf)
        print("URL:", result.markdown)
    
if __name__ == '__main__':
    asyncio.run(main())