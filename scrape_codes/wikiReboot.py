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
    movieGroups = soup.select('.mw-category-group')
    movieGroup = ''
    for i in movieGroups:
        movieGroup = movieGroup + str(i)
        
    p_a = '<li><a href="(.*?)" title=".*?">.*?</a></li>'
    p_title = '<li><a href=".*?" title="(.*?)">.*?</a></li>'
    a = re.findall(p_a, movieGroup, re.S)
    title = re.findall(p_title, movieGroup, re.S)
    for i in range(len(title)):
        films.append({'Reboot':title[i], 'href':a[i]})
        
    file = open(filename+'.csv', 'w', newline ='')
    with file:
        header = ['Reboot', 'href']
        writer = csv.DictWriter(file, fieldnames = header)
        writer.writeheader()
        for film in films:
            writer.writerow(film)

test_url = { 'reboot_films':'https://en.wikipedia.org/wiki/Category:Reboot_films'}

for key in test_url:
    scrape(key, test_url[key])
