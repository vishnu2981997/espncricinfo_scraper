import json

from scrapy.crawler import CrawlerProcess

from espncricinfo_scraper.spiders.player_details import PlayerDetailsSpider
import os
from collections import OrderedDict

import csv


def delete_file(file):
    try:
        os.remove(file)
    except Exception as exe:
        print(exe)


def read_json(file_name):
    data = []
    try:
        with open(file_name + '.json') as f:
            data = json.load(f)
    except Exception as exe:
        print(exe)

    return data


def main():
    settings = {
        'FEED_URI': "player_details.json",
        'FEED_FORMAT': 'json'
    }
    delete_file(settings["FEED_URI"])

    process = CrawlerProcess(settings=settings)

    process.crawl(PlayerDetailsSpider)
    process.start()

    players = read_json("player_details")

    print(players)

    unique_data = {}
    for player in players:
        if player["name"] not in unique_data:
            unique_data[player["name"]] = {"country": player["country"], "score": player["score"]}
        else:
            if unique_data[player["name"]]["score"] < player["score"]:
                unique_data[player["name"]]["score"] = player["score"]

    sorted_data = OrderedDict(sorted(unique_data.items(), key=lambda kv: kv[1]['score'], reverse=True))
    top_fifteen = []
    for item in sorted_data:
        top_fifteen.append({"name": item, "country": sorted_data[item]["country"], "score": sorted_data[item]["score"]})

    top_fifteen = top_fifteen[:15]

    with open('player_details.csv', mode='w') as csv_file:
        fieldnames = ['name', 'country', 'score']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for data in top_fifteen:
            writer.writerow(data)


if __name__ == "__main__":
    main()
