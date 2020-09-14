import scrapy


class TPSquadSpider(scrapy.Spider):
    name = "tpm-squad"
    start_urls = ['https://www.tpmazembe.com/fr/equipe/effectif']

    def parse(self, response):
        player_links = response.css('.joueurs div.joueur a::attr(href)').getall()
        yield from response.follow_all(player_links, callback=self.parse_squad)
        
    def parse_squad(self, response):
        statistics = []
        seasons = response.css('.statsjoueur thead th::text').getall()
        for i, season in enumerate(seasons):
            if i != 0 and i < len(seasons)-1:
                statistics.append({'season': season})

        statistics = self.get_stats(response, statistics)        
        details = self.get_details(response)
        yield {
            'image': response.css('.img-fluid::attr(src)').get(),
            'details': details,
            'number': response.css('h2 span::text').get(),
            'name': response.css('h2::text').get(),
            'clubs': response.css('.clubs p').get(),
            'palmares': response.css('.palmares::text').get(),
            'statistics': statistics
        }

    def get_stats(self, response, statistics):
        for attribute in response.css('.statsjoueur tbody tr'):
            attrName = attribute.css('strong::text').get()
            statType = ''
            if 'matchs' in str(attrName):
                statType = 'played'
            elif 'Titulaire' in str(attrName):
                statType = 'standing'
            elif 'Remplaçant' in str(attrName):
                statType = 'subtitute'
            elif 'Minutes' in str(attrName):
                statType = 'minutes'
            elif 'buts ' in str(attrName):
                statType = 'goals'
            elif 'Passes ' in str(attrName):
                statType = 'assists'
            elif 'Jaunes' in str(attrName):
                statType = 'yellow_card'
            elif 'Rouges' in str(attrName):
                statType = 'red_card'
            
            if (len(statType) > 0):
                for index, value in enumerate(attribute.css('.statschiffres::text').getall()):
                    if index < len(statistics):
                        statistics[index][statType] = value

        return statistics

    def get_details(self, response):
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

        return {
                'position': position,
                'birth': birth,
                'nationality': nationality,
                'since': since,
                'size': size,
                'weight': weight
            }
