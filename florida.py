from disaster_scrapers import Scraper
import requests
import json


class FplStormOutages(Scraper):
    owner = "simonw"
    repo = "disaster-data"
    filepath = "florida/fpl-storm-outages.json"

    url = "https://www.fplmaps.com/data/storm-outages.js"

    def fetch_data(self):
        content = requests.get(self.url, timeout=10).text
        # Stripe the 'define(' and ');'
        if content.startswith("define("):
            content = content.split("define(")[1]
        if content.endswith(");"):
            content = content.rsplit(");", 1)[0]
        return json.loads(content)


class FplCountyOutages(Scraper):
    owner = "simonw"
    repo = "disaster-data"
    filepath = "florida/fpl-county-outages.json"

    url = "https://www.fplmaps.com/customer/outage/CountyOutages.json"

    def fetch_data(self):
        return requests.get(self.url, timeout=10).json()
