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
    
    p_movie = '<h2><span class="mw-headline" id="Films">Films.*?</h2>(.*?)<h2>'
    movies = re.findall(p_movie, res, re.S)
    p_tr = '<tr>(.*?)</tr>'
    movies = re.findall(p_tr, movies[0], re.S)
    movies = movies[1:]
    p_contents = '<td.*?>(.*?)</td>'
    
    p_year = '([(].*?[)])'
    for movie in movies:
        pre = []
        ori = []
        movie_info = re.findall(p_contents, movie, re.S)

        prequel_year = re.findall(p_year, movie_info[0], re.S)
        soup_pre = BeautifulSoup(movie_info[0], 'html.parser')
        tb_pre = soup_pre.select('i')
        for i in range(len(tb_pre)):
            pre.append(tb_pre[i].text + prequel_year[i])
        
        original_year = re.findall(p_year, movie_info[1], re.S)
        soup_ori = BeautifulSoup(movie_info[1], 'html.parser')
        tb_ori = soup_ori.select('i')
        for i in range(len(tb_ori)):
            ori.append(tb_ori[i].text + original_year[i])
        films.append({'Prequel':pre, 'Original':ori})
        
    file = open(filename+'.csv', 'w', newline ='')
    with file:
        header = ['Prequel', 'Original']
        writer = csv.DictWriter(file, fieldnames = header)
        writer.writeheader()
        for film in films:
            writer.writerow(film)            

test_url = {'list of prequels':'https://en.wikipedia.org/wiki/List_of_prequels'}

for key in test_url:
    scrape(key, test_url[key])
