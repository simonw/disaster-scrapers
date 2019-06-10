from disaster_scrapers import Scraper
from bs4 import BeautifulSoup as Soup
import requests

# Just doing Sand Fire at the moment

class SandFire(Scraper):
    url = "http://www.fire.ca.gov/current_incidents/incidentdetails/Index/2322"
    owner = "simonw"
    repo = "disaster-data"
    filepath = "cal-fires/2322-sand-fire.json"

    def fetch_data(self):
        soup = Soup(requests.get(self.url).content, "html5lib")
        table = soup.select(".incident_table")[0]
        info = {
            "summary": table["summary"],
        }
        for tr in table.select("tr"):
            try:
                title = tr.select("td.emphasized")[0]
                info[title.text.strip().rstrip(":")] = title.find_next("td").text.strip()
            except:
                pass
        # Split out latitude and longitude, if available
        if "Long/Lat" in info:
            longitude, latitude = info["Long/Lat"].split("/")
            info["latitude"] = latitude
            info["longitude"] = longitude
        return info
