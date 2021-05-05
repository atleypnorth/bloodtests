import requests
from bs4 import BeautifulSoup
from time import sleep
import datetime
import logging
from argparse import ArgumentParser

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(levelname)s %(message)s")
_logger = logging.getLogger()


def parse_date(value):
    return datetime.datetime.strptime(value, '%Y%m%d').date()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('date_limit', type=parse_date, help="date limit in YYYYMMDD format")
    parser.add_argument('--sleep', type=int, default=180, help="seconds to wait between checks")
    args = parser.parse_args()

    while True:
        page = requests.get("https://www.swiftqueue.co.uk/bromley.php")
        soup = BeautifulSoup(page.text, 'html.parser')
        for row in soup.find_all(class_='search-result row'):
            next_avail = row.find_all(class_='next-avail-text')
            entry_time = next_avail[0].find('strong').string
            entry = next_avail[1].find('strong').string
            entry_date = datetime.datetime.strptime(entry, '%d-%m-%Y').date()
            where = row.find(class_='search-result-content col-md-3 col-xs-6').h3.string
            if entry_date < args.date_limit:
                _logger.warning(f' POSSIBLE! {entry_time.string}, {entry_date}, {where}')
        _logger.info('Done checking')
        sleep(args.sleep)
