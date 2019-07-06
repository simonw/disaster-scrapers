from disaster_scrapers import DeltaScraper
import requests


class SCEOutages(DeltaScraper):
    url = "https://prodms.dms.sce.com/outage/v1/power/outage"
    owner = "simonw"
    repo = "sce-outages"
    filepath = "sce-outages.json"

    record_key = "incidentId"
    noun = "incident"

    def fetch_data(self):
        data = requests.get(self.url, timeout=10).json()
        return data["outageMapDataResponse"]["AOCIncidents"]["incident"]

    def display_record(self, outage):
        display = []
        print(outpage)
        display.append(
            "  {incidentId} in {cityName} {countyName} affecting {numberOfCustomersAffected}".format(
                outage
            )
        )
        display.append(
            "    https://www.google.com/maps/search/{centroidY},{centroidX}".format(
                outage
            )
        )
        display.append(
            "    {memoCauseCodeDescription} - {crewStatusCodeDescription}".format(
                outage
            )
        )
        display.append("")
        return "\n".join(display)
