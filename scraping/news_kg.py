from parsel import Selector
import requests


class NewsScraper:
    START_URL = 'https://24.kg'
    LINK_XPATH = '//div[@class="col-xs-12"]/div/div/a/@href'

    def parse_data(self):
        text = requests.get(self.START_URL).text
        tree = Selector(text=text)
        links = tree.xpath(self.LINK_XPATH).extract()
        data = []
        for link in links:
            data.append(f'https://24.kg' + link)
        return data[:5]

