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
            href = movie.css('h3.lister-item-header > a::attr(href)').extract()
            film_link = self.initial_url + href[0]
            yield response.follow(url=film_link, callback=self.films, meta = {'puesto':puesto})

        next_page = response.css('div.desc > a.lister-page-next::attr(href)').extract()
        next_href = next_page[0]
        link = self.initial_url + next_href
        self.indice += 1
        if self.indice < 15:
            yield scrapy.Request(link, callback=self.parse)


    def films(self, response):
        titulo = response.css('div.sc-80d4314-0 > div.sc-80d4314-1 > h1.sc-b73cd867-0::text').get()
        directores = response.css("ul.sc-bfec09a1-8 li:nth-child(1) li a::text").getall()
        escritores = response.css("ul.sc-bfec09a1-8 li:nth-child(2) li a::text").getall()
        actores = response.css(".sc-bfec09a1-7 > a::text").getall()
        resenas = response.css("ul.sc-3ff39621-0 .score::text").getall()

        print(response.meta.get('puesto'), '-',titulo, '-', directores, '-', escritores, '-', actores, '-', resenas)
