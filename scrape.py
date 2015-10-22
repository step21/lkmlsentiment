from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import urlparse


def make_link_absolute(unabsolute_url, base_url):
    """
    Taken from http://stackoverflow.com/questions/4468410/python-beautifulsoup-equivalent-to-lxml-make-links-absolute
    """
    return urlparse.urljoin(base_url, unabsolute_url)


def scrape():
    """
    """
    start_datetime = datetime(year=2010, month=1, day=1, hour=0, minute=0, second=0)
    base_url = "https://lkml.org/lkml/{year}/{month}/{day}"

    for day_count in [0]:
        current_datetime = start_datetime + timedelta(days=day_count)
        lkml_archive_day_url = base_url.format(year=current_datetime.year, month=current_datetime.month, day=current_datetime.day)
        lkml_day_message_set = set()
        day_http_request = requests.get(lkml_archive_day_url)
        soup = BeautifulSoup(day_http_request.text, "html.parser")
        for a_tag in soup.find_all("a"):
            tag_href = a_tag.get("href")
            if "{year}/{month}/{day}/".format(year=current_datetime.year, month=current_datetime.month, day=current_datetime.day) in str(tag_href) and tag_href not in lkml_day_message_set:
                lkml_day_message_set.add(tag_href)
                message_archive_url = make_link_absolute(tag_href, lkml_archive_day_url)
                message_http_request = requests.get(message_archive_url)
                message_soup = BeautifulSoup(message_http_request.text, "html.parser")
                try:
                    subject = message_soup.findAll("td", text="Subject")[0].findNext("td").text
                except:
                    continue
                print message_archive_url, subject


if __name__ == "__main__":
    scrape()