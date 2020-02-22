import csv
import json
import os
from collections import OrderedDict

from scrapy.crawler import CrawlerProcess

from espncricinfo_scraper.spiders.player_details import PlayerDetailsSpider


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

    unique_data = {}

    for player in players:
        if player["name"] not in unique_data:
            unique_data[player["name"]] = {
                "country": player["country"],
                "score": [player["score"]],
                "max_runs": player["score"]["runs"],
                "max_runs_year": player["score"]["year"]
            }
        else:
            if unique_data[player["name"]]["max_runs"] < player["score"]["runs"]:
                unique_data[player["name"]]["max_runs"] = player["score"]["runs"]
                unique_data[player["name"]]["max_runs_year"] = player["score"]["year"]
            unique_data[player["name"]]["score"].append(player["score"])

    sorted_data = OrderedDict(sorted(unique_data.items(), key=lambda kv: kv[1]['max_runs'], reverse=True))

    start_year = 1972
    end_year = 2020

    formatted_data = []
    for item in sorted_data:
        player_data = {
            "name": item,
            "country": sorted_data[item]["country"],
        }
        scores = {}
        for score in sorted_data[item]["score"]:
            scores[score["year"]] = score["runs"]

        for year in range(start_year, end_year + 1):
            player_data[str(year)] = scores[year] if scores.get(year, None) else "-"

        formatted_data.append(player_data)

    with open('player_details.csv', mode='w') as csv_file:
        fieldnames = ['name', 'country']
        years = [str(i) for i in range(start_year, end_year + 1)]
        fieldnames += years
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for data in formatted_data:
            writer.writerow(data)


if __name__ == "__main__":
    main()
