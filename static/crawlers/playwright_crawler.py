from playwright.async_api import async_playwright
import asyncio, json

async def crawl_website(url, max_pages=50):
    crawled_data, visited_urls, to_visit = [], set(), [url]
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        async def crawl_single_page(page_url):
            if page_url in visited_urls: return
            visited_urls.add(page_url)
            page = await context.new_page()
            try:
                await page.goto(page_url, timeout=60000)
                crawled_data.append({'url': page_url,'title': await page.title(),'headings': await page.locator('h1, h2, h3').all_inner_texts(),'meta_description': await page.locator('meta[name="description"]').get_attribute('content'),'content': await page.content()})
                links = await page.locator('a').evaluate_all('elements => elements.map(el => el.href)')
                to_visit.extend([link for link in links if link.startswith(url) and link not in visited_urls])
            except Exception as e:
                print(f"Failed: {e}")
            finally:
                await page.close()

        tasks = []
        for _ in range(min(max_pages, len(to_visit))):
            tasks.append(asyncio.create_task(crawl_single_page(to_visit.pop(0))))
        await asyncio.gather(*tasks)
        await browser.close()

    with open('output/output.json', 'w') as f: json.dump(crawled_data, f, indent=4)
