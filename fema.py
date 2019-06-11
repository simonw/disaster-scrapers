from disaster_scrapers import DeltaScraper
import requests


class FemaShelters(DeltaScraper):
    url = "https://gis.fema.gov/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=FEMA:FEMANSSOpenShelters&maxFeatures=250&outputFormat=json&_=1560122418173"
    owner = "simonw"
    repo = "disaster-data"
    filepath = "fema/shelters.json"

    record_key = "SHELTER_ID"
    noun = "shelter"

    def fetch_data(self):
        data = requests.get(self.url, timeout=10).json()
        return [feature["properties"] for feature in data["features"]]

    def display_record(self, record):
        display = []
        display.append(
            "  {SHELTER_NAME} in {CITY}, {STATE} ({SHELTER_STATUS})".format(**record)
        )
        display.append(
            "    https://www.google.com/maps/search/{LATITUDE},{LONGITUDE}".format(
                **record
            )
        )
        display.append("    population = {TOTAL_POPULATION}".format(**record))
        display.append("")
        return "\n".join(display)
