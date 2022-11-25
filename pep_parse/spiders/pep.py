import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_group = response.css('a.pep.reference.internal::attr(href)')[1:]
        for link_group in all_group:
            yield response.follow(link_group, self.parse_pep)

    def parse_pep(self, response):
        data = {
            'number': response.css('h1.page-title::text').get().split()[1],
            'name': response.css(
                'h1.page-title::text'
            ).get().split(' – ')[1],
            'status': response.css('dt:contains("Status") + dd::text').get()
        }
        yield PepParseItem(data)
