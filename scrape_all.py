from disaster_scrapers import Scraper
import pathlib
import importlib
import os


def discover_scrapers():
    scrapers = []
    for filepath in pathlib.Path(".").glob("*.py"):
        mod = importlib.import_module(filepath.stem)
        for klass in mod.__dict__.values():
            try:
                if issubclass(klass, Scraper) and klass.__module__ != "disaster_scrapers":
                    scrapers.append(klass)
            except TypeError:
                pass
    return scrapers


if __name__ == "__main__":
    TOKEN = os.environ["GITHUB_TOKEN"]
    for scraper_class in discover_scrapers():
        scraper = scraper_class(TOKEN)
        scraper.scrape_and_store()
