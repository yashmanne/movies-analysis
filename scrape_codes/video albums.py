import re
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import csv

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

def scrape(filename, url, year):
    films = []
    res = requests.get(url,headers=headers)
    res.encoding = 'utf-8'
    res = res.text
    soup = BeautifulSoup(res, 'html.parser')
    tb = soup.select('#mw-pages .mw-category-group li a')
    for i in tb:
        films.append({'Title':i.text, 'Year': str(year)})
    
    file = open(filename+'.csv', 'a', newline ='')
    with file:
        header = ['Title', 'Year']
        writer = csv.DictWriter(file, fieldnames = header)
        # writer.writeheader()
        for film in films:
            try:
                writer.writerow(film)
            except:
                print(film['Title'] + ' ' + film['Year'])
            
ova_years = list(range(1979,2023))

for year in ova_years:
    key = 'video albums'
    url = 'https://en.wikipedia.org/wiki/Category:'+ str(year) +'_video_albums'
    scrape(key, url, year)
