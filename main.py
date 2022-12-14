import re
import datetime
import csv
import argparse
import logging
import news_page_objects as news
from common import config

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
is_well_formed_link = re.compile(r'^https?//.+/.+$') # https://example.com/hello
is_root_path = re.compile(r'^/.+$') # /some-text
is_other_host = re.compile(r'^https?://.+/$')

def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']
    logging.info('Beginning scrape for {}'.format(host))
    homepage = news.HomePage(news_site_uid, host)

    articles = []
    list_link = homepage.article_links
    i = 0
    for link in list_link:
        i += 1
        article = _fetch_article(news_site_uid, host, link)
        if article:
            logger.info('Article fetched!!!')
            articles.append(article)
            if i == 10:
                break
            # print(article.title)
    _save_articles(news_site_uid, articles)


def _save_articles(news_site_uid, articles):
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    out_file_name = f'{news_site_uid}_{now}_articles.csv'
    csv_headers = list(filter(lambda property: not property.startswith('_'), dir(articles[0])))
    with open(out_file_name, 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

        for article in articles:
            row = [str(getattr(article, prop)) for prop in csv_headers]
            writer.writerow(row)

def _fetch_article(news_site_uid, host, link):
    
    link_format = _build_link(host, link)
    logger.info(f'Start fetching article at {link_format}')

    article = None
    try:
        article = news.ArticlePage(news_site_uid, link_format)

    except (HTTPError, MaxRetryError) as e :
        logger.warning('Error while fetching the article', exc_info=False)
    
    if article and not article.body:
        logger.warning('Invalid article. There is not body')
        return None
    return article

def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_other_host.match(link):
        return link
    elif is_root_path.match(link):
        return f'{host}{link}'
    else:
        return f'{host}/{link}'


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()

    # news_site_choices = list(config()['news_sites'].keys())
    # parser.add_argument('news_site', help='The news site that you want to scrape',
    #                     type=str, choices=news_site_choices)
    # args = parser.parse_args()
    _news_scraper('elpais')
