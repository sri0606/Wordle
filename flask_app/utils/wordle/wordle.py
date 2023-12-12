import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def scrape_word_of_day():
    url = 'https://www.merriam-webster.com/word-of-the-day'

    # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        word_header = soup.find('h2', class_='word-header-txt')

        if word_header:
            word_of_the_day = word_header.text.strip()
            return word_of_the_day
        else:
            return None
    else:
        print(f'Failed to retrieve the web page. Status code: {response.status_code}')

def spell_check(word):
    '''
    USing Words API which can be accessed free through Rapid API website

    Alternatively you can use pyenchant too.
    '''

    #code from rapidAPI website

    url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/definitions"

    headers = {
        "X-RapidAPI-Key": os.environ.get("RAPID_API_KEY"),
        "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    #word exists
    if response.status_code==200:
        return {'spelling_correct':1}
    else:
        return {'spelling_correct':0}
