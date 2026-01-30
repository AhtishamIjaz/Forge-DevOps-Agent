import pytest
from main import scrape_hacker_news
from unittest.mock import patch, MagicMock
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import csv

def test_scrape_hacker_news_success():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body><a class="storylink">Test Title</a></body></html>'
        mock_get.return_value = mock_response

        with patch('csv.writer') as mock_writer:
            mock_writer.return_value.writerow.side_effect = lambda *args: None
            scrape_hacker_news()

            mock_writer.return_value.writerow.assert_called_once_with(['Title', 'Timestamp'])
            mock_writer.return_value.writerow.assert_called_with(['Test Title', datetime.now()])

def test_scrape_hacker_news_failure():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        scrape_hacker_news()

        with open('error_log.txt', 'r') as log_file:
            log_content = log_file.read()
            assert 'Error: Unable to reach website at' in log_content

def test_scrape_hacker_news_empty_response():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = ''
        mock_get.return_value = mock_response

        scrape_hacker_news()

        with open('hacker_news.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            assert list(reader) == [['Title', 'Timestamp']]

def test_scrape_hacker_news_invalid_url():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body></body></html>'
        mock_get.return_value = mock_response

        scrape_hacker_news()

        with open('error_log.txt', 'r') as log_file:
            log_content = log_file.read()
            assert 'Error: Unable to reach website at' in log_content

def test_scrape_hacker_news_invalid_status_code():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        scrape_hacker_news()

        with open('error_log.txt', 'r') as log_file:
            log_content = log_file.read()
            assert 'Error: Unable to reach website at' in log_content

def test_scrape_hacker_news_invalid_request():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.RequestException('Test Exception')
        scrape_hacker_news()

        with open('error_log.txt', 'r') as log_file:
            log_content = log_file.read()
            assert 'Error: Test Exception at' in log_content

def test_scrape_hacker_news_csv_write_failure():
    with patch('csv.writer') as mock_writer:
        mock_writer.side_effect = csv.Error('Test CSV Error')
        with pytest.raises(csv.Error):
            scrape_hacker_news()

def test_scrape_hacker_news_csv_write_empty():
    with patch('csv.writer') as mock_writer:
        mock_writer.return_value.writerow.side_effect = lambda *args: None
        scrape_hacker_news()

        with open('hacker_news.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            assert list(reader) == [['Title', 'Timestamp']]

def test_scrape_hacker_news_csv_write_invalid():
    with patch('csv.writer') as mock_writer:
        mock_writer.return_value.writerow.side_effect = lambda *args: None
        scrape_hacker_news()

        with open('hacker_news.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            assert list(reader) == [['Title', 'Timestamp']]