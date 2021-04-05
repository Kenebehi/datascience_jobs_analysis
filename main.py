import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup


def extract(page):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0"}
    url = "https://uk.indeed.com/jobs?q=data&start={page}"
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def transform(soup):
    divs = soup.find_all('div', class_='jobsearch-SerpJobCard')
    for div in divs:
        title = div.find('a').text.strip()
        company = div.find('span', class_='company').text.strip()
        date_posted = div.find('span', class_='date').text.strip()
        try:
            summary = div.find('span', class_='summary').text.strip().replace('\n', '')
        except AttributeError:
            summary = ''
        try:
            salary = div.find('span', class_='salaryText').text.strip()
        except AttributeError:
            salary = ''
        job = {
            "title": title,
            "company": company,
            "salary": salary,
            "summary": summary,
            "date_posted": date_posted,
            "time_stamp": datetime.datetime.now()
        }
        joblist.append(job)
    print(joblist)
    return


joblist = []

for i in range(0, 40, 10):
    c = extract(0)
    transform(c)

df = pd.DataFrame(joblist)
print(df.head())

df.to_csv('/home/kenneth/Downloads/indeed.csv')
