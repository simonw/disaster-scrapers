from disaster_scrapers import Scraper
from bs4 import BeautifulSoup as Soup
import requests


class FireScraper(Scraper):
    owner = "simonw"
    repo = "disaster-data"

    def __init__(self, token, incident_id, name):
        self.incident_id = incident_id
        self.filepath = "cal-fires/{}-{}.json".format(
            self.incident_id, name.lower().strip().replace(" ", "-")
        )
        super().__init__(token)

    def fetch_data(self):
        soup = Soup(
            requests.get(
                "http://www.fire.ca.gov/current_incidents/incidentdetails/Index/{}".format(
                    self.incident_id
                )
            ).content,
            "html5lib",
        )
        table = soup.select(".incident_table")[0]
        info = {"summary": table["summary"]}
        for tr in table.select("tr"):
            try:
                title = tr.select("td.emphasized")[0]
                info[title.text.strip().rstrip(":")] = title.find_next(
                    "td"
                ).text.strip()
            except:
                pass
        # Split out latitude and longitude, if available
        if "Long/Lat" in info:
            longitude, latitude = info["Long/Lat"].split("/")
            info["latitude"] = latitude
            info["longitude"] = longitude
        return info


def load_scrapers(token):
    # Scrape the list of fires
    url = "http://www.fire.ca.gov/current_incidents/"
    page = 1
    incidents = []  # List of (id, name) tuples
    while True:
        html = requests.get("{}?page={}".format(url, page)).text
        soup = Soup(html, "html5lib")
        scraped_incidents = [
            (t.get("id"), t.get("title"))
            for t in soup.select("table.incident_table")
            if t.get("id")
        ]
        if not scraped_incidents:
            break
        incidents.extend(scraped_incidents)
        page += 1
        if "?page={}".format(page) not in html:
            break
        if page > 100:
            break
    # Return a scraper for each incident
    return [FireScraper(token, incident_id, name) for incident_id, name in incidents]
