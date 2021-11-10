import requests
import bs4

def scraping__inf_button():
    try:
        response = requests.get('https://www.directoriocubano.info/cita/')
        html_page = bs4.BeautifulSoup(response.text, 'html.parser')
        is_button_active = html_page.select()
    except e:
        print(e)
if __name__ == '__main__':
    scraping__inf_button()
