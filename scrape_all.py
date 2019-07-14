from disaster_scrapers import Scraper
import pathlib
import importlib
import os
import sys


def discover_scrapers(token):
    scrapers = []
    for filepath in pathlib.Path(".").glob("*.py"):
        mod = importlib.import_module(filepath.stem)
        # if there's a load_scrapers() function, call that
        if hasattr(mod, "load_scrapers"):
            scrapers.extend(mod.load_scrapers(token))
        # Otherwise instantiate a scraper for each class
        else:
            for klass in mod.__dict__.values():
                try:
                    if (
                        issubclass(klass, Scraper)
                        and klass.__module__ != "disaster_scrapers"
                    ):
                        scrapers.append(klass(token))
                except TypeError:
                    pass
    return scrapers


if __name__ == "__main__":
    github_token = os.environ.get("GITHUB_TOKEN")
    for scraper in discover_scrapers(github_token):
        if github_token is None:
            scraper.test_mode = True
        try:
            scraper.scrape_and_store()
        except Exception as e:
            print(scraper.filepath, file=sys.stderr)
            print(e, file=sys.stderr)
            print("\n", file=sys.stderr)
