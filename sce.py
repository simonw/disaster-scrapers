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
        # Need to .strip() trailing whitespace from county
        fixed = {**outage, **{"countyName": (outage.get("countyName") or "").strip()}}
        display = []
        display.append(
            "  {incidentId} in {cityName} {countyName} affecting {numberOfCustomersAffected}".format(
                **fixed
            )
        )
        display.append(
            "    https://www.google.com/maps/search/{centroidY},{centroidX}".format(
                **fixed
            )
        )
        display.append(
            "    {memoCauseCodeDescription} - {crewStatusCodeDescription}".format(
                **fixed
            )
        )
        display.append("")
        return "\n".join(display)
