#Scrapping a Real Website
from bs4 import BeautifulSoup 
import requests
import time

def find_jobs():
    url = 'https://inshorts.com/en/read'
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('div', itemscope=True, itemtype="http://schema.org/NewsArticle")

    
    # Convert the ResultSet to a string
    jobs_str = '\n'.join(str(job) for job in jobs)
    
    # Open the file with UTF-8 encoding
    with open('file.txt', 'w', encoding='utf-8') as f:
        f.write(jobs_str)

if __name__ == '__main__':
    while True:
        find_jobs()