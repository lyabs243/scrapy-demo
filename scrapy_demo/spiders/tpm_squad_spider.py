import scrapy


class TPSquadSpider(scrapy.Spider):
    name = "tpm-squad"
    start_urls = ['https://www.tpmazembe.com/fr/equipe/effectif']

    def parse(self, response):
        player_links = response.css('.joueurs div.joueur a::attr(href)').getall()
        yield from response.follow_all(player_links, callback=self.parse_squad)
        
    def parse_squad(self, response):
        yield {
            'image': response.css('.img-fluid::attr(src)').get(),
            'name': response.css('h2::text').get(),
            'clubs': response.css('.clubs p').get(),
            'palmares': response.css('.palmares::text').get()
        }