from disaster_scrapers import DeltaScraper
import requests


class DukeEnergyScraper(DeltaScraper):
    owner = "simonw"
    repo = "disaster-data"

    record_key = "areaOfInterestId"
    show_changes = True
    noun = "county summary"
    plural = "county summaries"

    def __init__(self, token, jurisdiction, filepath):
        self.jurisdiction = jurisdiction
        self.filepath = filepath
        super().__init__(token)

    def fetch_data(self):
        url = "https://cust-api.duke-energy.com/outage-maps/v1/counties?jurisdiction={}".format(
            self.jurisdiction
        )
        county_summaries = requests.get(
            url,
            headers={
                "Authorization": "Basic OXUxRmdtcXJNVlBJUEZGeE41aVZJbEFmRHpoMDhNQlI6Y1g0QTJmeFdXMG5XVlRhNg=="
            },
        ).json()["data"]
        # Flatten out the nested "areaOfInterestSummary" array
        for county_summary in county_summaries:
            summary = county_summary.pop("areaOfInterestSummary")
            for key, value in summary.items():
                county_summary["summary_{}".format(key)] = value
        return county_summaries


def load_scrapers(token):
    return [
        DukeEnergyScraper(token, "DEC", "duke-energy/Duke-Energy-Carolinas.json"),
        DukeEnergyScraper(token, "DEF", "duke-energy/Duke-Energy-Florida.json"),
    ]
