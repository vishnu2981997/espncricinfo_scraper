# -*- coding: utf-8 -*-
import scrapy


class PlayerDetailsSpider(scrapy.Spider):
    name = 'player_details'
    allowed_domains = ['stats.espncricinfo.com']
    start_year = 1971
    end_year = 2020
    start_urls = ['http://stats.espncricinfo.com/ci/engine/records/batting/most_runs_career.html?class=2;id=' + str(
        i) + ';type=year' for i in range(start_year, end_year + 1)]
    custom_settings = {'FEED_URI': "player_details.json",
                       'FEED_FORMAT': 'json'}

    def parse(self, response):
        player_name = response.xpath("//table//tbody//tr//td//a/text()").extract()
        countries = [i.strip() for i in response.xpath("//table//tbody//tr//td[1]/text()").extract()]
        scores = [i.strip("*") for i in response.xpath("//table//tbody//tr//td//b/text()").extract()]

        row_data = zip(player_name, countries, scores)

        for item in row_data:
            scraped_info = {
                'name': item[0],
                'country': item[1],
                'score': int(item[2]),
            }

            yield scraped_info
