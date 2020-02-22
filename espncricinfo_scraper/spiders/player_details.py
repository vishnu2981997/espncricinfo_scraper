# -*- coding: utf-8 -*-
import scrapy
import urllib.parse as urlparse
from urllib.parse import parse_qs


class PlayerDetailsSpider(scrapy.Spider):
    name = 'player_details'
    allowed_domains = ['stats.espncricinfo.com']
    start_year = 1972
    end_year = 2020
    start_urls = [
        "http://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;filter=advanced;orderby=runs;size=15;spanmax1=01+Jan+" + str(
            i) + ";spanmin1=01+Jan+1970;spanval1=span;template=results;type=batting" for i in
        range(start_year, end_year + 1)]
    custom_settings = {'FEED_URI': "player_details.json",
                       'FEED_FORMAT': 'json'}

    def parse(self, response):
        player_name = response.xpath("//table//tbody//tr//td//a/text()").extract()
        countries = [i.strip() for i in response.xpath("//table//tbody//tr//td[1]/text()").extract()]
        scores = [i.strip("*") for i in response.xpath("//table//tbody//tr//td//b/text()").extract()]

        row_data = zip(player_name, countries, scores)

        url = response.url
        parsed = urlparse.urlparse(url)
        year = parse_qs(parsed.query)['spanmax1'][0].split()[-1]
        for item in row_data:
            scraped_info = {
                'name': item[0],
                'country': item[1],
                'score': {"year": int(year), "runs": int(item[2])},
            }

            yield scraped_info
