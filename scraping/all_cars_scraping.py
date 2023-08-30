from parsel import Selector
import httpx
import asyncio


class AllCarsScraping:
    START_URL = 'https://www.mashina.kg/'
    PLUS_URL = 'https://www.mashina.kg'
    LINK_XPATH = '//div[@class="after-logo-2"]/ul/li/a/@href'
    CATEGORY_XPATH = '//ul[@class="login-submenu"]//li/a/@href'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': 'PHPSESSID=25qvvq4og0jbl52uqdhnsbk4ut; device_view=full; hl=en'
    }

    async def generate_link(self, links):
        for link in links:
            yield link

    async def get_url(self, client, url):
        response = await client.get(url)
        await self.parse_links(content=response.text)
        return response

    async def parse_links(self, content):
        tree = Selector(text=content)
        links = tree.xpath(self.LINK_XPATH).extract()
        print('Ссылки на категории:')
        for link in links:
            print(self.PLUS_URL+link)
        await self.parse_categories(content=content)

    async def parse_categories(self,content):
        tree = Selector(text=content)
        category_links = tree.xpath(self.CATEGORY_XPATH).extract()
        print('\nСсылки на тип категории:')
        for category_link in category_links:
            print(self.PLUS_URL+category_link)

    async def parse_data(self):
        async with httpx.AsyncClient(headers=self.HEADERS) as client:
            await self.get_url(client=client, url=self.START_URL)


if __name__ == "__main__":
    scraper = AllCarsScraping()
    asyncio.run(scraper.parse_data())
