from disaster_scrapers import DeltaScraper
import requests


class PGEOutages(DeltaScraper):
    url = "https://apim.pge.com/cocoutage/outages/getOutagesRegions?regionType=city&expand=true"
    owner = "simonw"
    repo = "pge-outages"
    filepath = "pge-outages.json"

    record_key = "outageNumber"
    noun = "outage"

    def fetch_data(self):
        data = requests.get(self.url, timeout=10).json()
        # Flatten into a list of outages
        outages = []
        for region in data["outagesRegions"]:
            for outage in region["outages"]:
                outage["regionName"] = region["regionName"]
                outages.append(outage)
        return outages

    def display_record(self, outage):
        display = []
        display.append(
            "  %(outageNumber)s in %(regionName)s affecting %(estCustAffected)s"
            % outage
        )
        display.append(
            "    https://www.google.com/maps/search/%(latitude)s,%(longitude)s" % outage
        )
        display.append("    %(cause)s - %(crewCurrentStatus)s" % outage)
        display.append("")
        return "\n".join(display)
