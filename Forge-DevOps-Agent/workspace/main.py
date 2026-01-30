import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def scrape_hacker_news():
    try:
        response = requests.get('https://news.ycombinator.com/')
        if response.status_code != 200:
            with open('error_log.txt', 'a') as log_file:
                log_file.write(f'Error: Unable to reach website at {datetime.now()}\n')
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        titles = [title.text for title in soup.find_all('a', class_='storylink')]

        with open('hacker_news.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Title', 'Timestamp'])
            for title in titles:
                writer.writerow([title, datetime.now()])

    except Exception as e:
        with open('error_log.txt', 'a') as log_file:
            log_file.write(f'Error: {str(e)} at {datetime.now()}\n')

if __name__ == '__main__':
    scrape_hacker_news()