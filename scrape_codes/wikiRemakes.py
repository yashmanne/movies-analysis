import re
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import csv

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

def scrape(filename, url):
    films = []
    res = requests.get(url,headers=headers)
    res.encoding = 'utf-8'
    res = res.text
    soup = BeautifulSoup(res, 'html.parser')
    tb = soup.select('tr')
    
    for i in range(len(tb)):
        
        text = tb[i].text
        if(text=='\nOriginal\nRemake(s)\nNotes\n'):
            continue
        info = text.split('\n')
        if len(info) >= 6:
            films.append({'Original':info[1], 'Remake(s)':info[3], 'Notes':info[5]})
        else:
            films.append({'Original':info[1], 'Remake(s)':info[3], 'Notes':''})
    file = open(filename+'.csv', 'w', newline ='')
    with file:
        header = ['Original', 'Remake(s)', 'Notes']
        writer = csv.DictWriter(file, fieldnames = header)
        writer.writeheader()
        for film in films:
            
            writer.writerow(film)

test_url = {'list of film remakes':'https://en.wikipedia.org/wiki/List_of_film_remakes_(A%E2%80%93M)'}

for key in test_url:
    scrape(key, test_url[key])
