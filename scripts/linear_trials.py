import re
import urllib.request
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

url = 'https://www.linear.org.au/trials/'
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, 'html.parser')
containers = soup.find_all('ul')
text = []
for line in containers:
    text.append(line.get_text())

# Find index of element at end of trial listings
index_start = [idx for idx, s in enumerate(text) if 'Media Enquiries' in s][-1]
# Find index of element at end of trial listings
index_end = [idx for idx, s in enumerate(text) if 'About Us' in s][0]
text = text[index_start+1:index_end]
text
