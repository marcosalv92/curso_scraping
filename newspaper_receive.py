import pandas as pd
from urllib.parse import urlparse
import argparse
import logging
logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)


def main(filename):
    logger.info('Starting cleaning process')
    df = _read_data(filename)
    newspaper_uid = _extract_newspaper_uid(filename)
    df = _add_newspaper_uid_column(df, newspaper_uid)
    df = _extract_host(df)
    df = _fill_missing_title(df)
    return df


def _fill_missing_title(df):
    logger.info('Filling missing title')
    missing_titles_mask = df['title'].isna()
    missing_titles = (df[missing_titles_mask]['url'].str.extract(
        r'(?P<missing_titles>[^/]+)$')).applymap(str).applymap(lambda title: title.replace('-', ' '))
    df.loc[missing_titles_mask, 'title'] = missing_titles.loc[:, 'missing_titles']
    return df


def _extract_host(df):
    logger.info('Extracting host from urls')
    df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)
    return df


def _add_newspaper_uid_column(df, newspaper_uid):
    logger.info(f'Filling newspaper_uid column with {newspaper_uid}')
    df['newspaper_uid'] = newspaper_uid
    return df


def _extract_newspaper_uid(filename):
    logger.info('Extracting newspaper uid')
    newspaper_uid = filename.split('_')[0]
    logger.info(f'Newspaper uid detected: {newspaper_uid}')
    return newspaper_uid


def _read_data(filename):
    logger.info(f'Reading file {filename}')
    return pd.read_csv(filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filename', help='The path to the dirty data', type=str)
    arg = parser.parse_args()
    df = main(arg.filename)
    print(df)
