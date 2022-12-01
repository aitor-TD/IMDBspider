import scrapy
from scrapy.http import Request


class ImdbSpider(scrapy.Spider):
    name = 'imdb'
    allowed_domains = ['www.imdb.com']
    initial_url = 'https://www.imdb.com/'
    start_urls = ['https://www.imdb.com/search/title/?genres=comedy&explore=title_type,genres']
    indice = 0

    def parse(self, response):
        movies = response.css('div.lister-item > div.lister-item-content')
        for movie in movies:
            puesto = movie.css('h3.lister-item-header > span.lister-item-index::text').get()
            titulo = movie.css('h3.lister-item-header > a::text').get()
            href = movie.css('h3.lister-item-header > a::attr(href)').extract()
            film_link = self.initial_url + href[0]
            yield scrapy.Request(film_link, callback=self.films)
            print(puesto, '-', titulo, '-', film_link, '-',)

        next_page = response.css('div.desc > a.lister-page-next::attr(href)').extract()
        next_href = next_page[0]
        link = self.initial_url + next_href
        self.indice += 1
        if self.indice < 5:
            yield scrapy.Request(link, callback=self.parse)

    def films(self, response):
        print('HOLA')