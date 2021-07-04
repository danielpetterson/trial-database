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
