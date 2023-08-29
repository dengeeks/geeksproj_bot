from parsel import Selector
import httpx
import asyncio


class CarsScraping:
    START_URL = 'https://www.mashina.kg/en/search/all/?page={}'
    LINK_XPATH = '//div[@class="list-item list-label"]/a/@href'
    HEADERS = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
          'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
          'Accept-Encoding': 'gzip, deflate, br',
          'Cookie': 'PHPSESSID=25qvvq4og0jbl52uqdhnsbk4ut; device_view=full; hl=en'
           }

    async def generate_page(self):
        for page in range(1,5+1):
            yield page

    async def get_url(self,client,url):
        response = await client.get(url)
        await self.parse_links(content=response.text)
        return response

    async def parse_links(self, content):
        tree = Selector(text=content)
        links = tree.xpath(self.LINK_XPATH).extract()
        return links

    async def parse_data(self):
        async with httpx.AsyncClient(headers=self.HEADERS) as client:
            async for page in self.generate_page():
                data = []
                response = await self.get_url(client=client, url=self.START_URL.format(page))
                links = await self.parse_links(content=response.text)
                for link in links:
                    data.append("https://www.mashina.kg" + link)
        return data[:5]




if __name__ == "__main__":
    scraper = CarsScraping()
    asyncio.run(scraper.parse_data())
