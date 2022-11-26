import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        trs = response.css('section[id=numerical-index]').css(
            'tbody').css('tr')
        for tr in trs:
            pep_link = tr.css('a').attrib['href']
            yield response.follow(pep_link, self.parse_pep)

    def parse_pep(self, response):
        data = {
            'number': response.css('h1.page-title::text').get().split()[1],
            'name': response.css(
                'h1.page-title::text'
            ).get().split(' – ')[1],
            'status': response.css('dt:contains("Status") + dd::text').get()
        }
        yield PepParseItem(data)
