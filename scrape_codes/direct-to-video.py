import re
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import csv

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
length = []
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
            writer.writerow(film)
            
dtv_years = list(range(1979,2024))
dtv_years.remove(1979)
dtv_years.remove(1981)
dtv_years.remove(2023)


for year in dtv_years:
    key = 'direct to video'
    url = 'https://en.wikipedia.org/wiki/Category:'+str(year)+'_direct-to-video_films'
    scrape(key, url, year)

