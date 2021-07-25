import re
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from help_funcs import find_between, strip_post_num, strip_pre_colon, total_days

url = "https://www.praclinicaltrials.com/about-pra/the-researches"

html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

tags = soup.find_all('a')

all_links = []
for tag in tags:
    all_links.append(tag.get('href'))

href_index = [idx for idx, s in enumerate(all_links) if 'researches/' in s]
link_list = all_links[href_index[0]:(href_index[-1]+1)]

links = []
for elem in link_list:
    link = ('https://www.praclinicaltrials.com' + elem)
    links.append(link)

total_soup = []
for url in links:
    link_html = urllib.request.urlopen(url)
    link_soup = BeautifulSoup(link_html, 'html.parser')
    total_soup.append(link_soup)

eligibility_list =[]
for soup in total_soup:
    text = soup.text.split("\t")
    index_eligibility = [idx for idx, s in enumerate(text) if 'Who can participate?' in s]
    if len(index_eligibility) < 1:
        index_eligibility = [idx for idx, s in enumerate(text) if 'Particulars' in s]
    eligibility = [text[i] for i in index_eligibility]
    elig_string = eligibility[-1].replace("\xa0", "").split('participate?')[-1].split('articulars')[-1].split("\n")
    eligibility_list.append(elig_string)

# removing empty strings
eligibility_cleaned = []
for elem in eligibility_list:
    elem = [item for item in elem if item]
    eligibility_cleaned.append(elem)
eligibility_cleaned
