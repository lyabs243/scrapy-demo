import scrapy


class TPSquadSpider(scrapy.Spider):
    name = "tpm-squad"
    start_urls = ['https://www.tpmazembe.com/fr/equipe/effectif']

    def parse(self, response):
        player_links = response.css('.joueurs div.joueur a::attr(href)').getall()
        yield from response.follow_all(player_links, callback=self.parse_squad)
        
    def parse_squad(self, response):
        
        player_details = response.css('.data-fiche li')
        for detail in player_details:
            img = detail.css('img::attr(src)').get()
            if 'poste' in img:
                position = detail.css('strong::text').get()
            elif 'naissance' in img:
                birth = detail.css('strong::text').get()
            elif 'nationalite' in img:
                nationality = detail.css('strong::text').get()
            elif 'clubdepuis' in img:
                since = detail.css('strong::text').get()
            elif 'taille' in img:
                size = detail.css('strong::text').get()
            elif 'poids' in img:
                weight = detail.css('strong::text').get()

        yield {
            'image': response.css('.img-fluid::attr(src)').get(),
            'details': {
                'position': position,
                'birth': birth,
                'nationality': nationality,
                'since': since,
                'size': size,
                'weight': weight
            },
            'number': response.css('h2 span::text').get(),
            'name': response.css('h2::text').get(),
            'clubs': response.css('.clubs p').get(),
            'palmares': response.css('.palmares::text').get()
        }