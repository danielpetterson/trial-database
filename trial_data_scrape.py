import pandas as pd
import re
import urllib.request
from bs4 import BeautifulSoup
from html_table_parser.parser import HTMLTableParser

###---------------------- AUS DataFrame -----------------------------
# defining the html contents of a URL.
#xhtml_adel = url_get_contents('https://www.cmax.com.au/current-trial/cm1520-part-a2/').decode('utf-8')
# xhtml_melb = url_get_contents('https://www.nucleusnetwork.com/au/participate-in-a-trial/melbourne-clinical-trials/').decode('utf-8')
# xhtml_bris = url_get_contents('https://www.nucleusnetwork.com/au/participate-in-a-trial/brisbane-clinical-trials/')
# .decode('utf-8')
# xhtml_sydn = url_get_contents('http://www.scientiaclinicalresearch.com.au/healthy-volunteers/')
# .decode('utf-8')
# xhtml_prth = url_get_contents('https://www.linear.org.au/trials/')
# .decode('utf-8')


html_melb = urllib.request.urlopen('https://www.nucleusnetwork.com/au/participate-in-a-trial/melbourne-clinical-trials/')
melb_soup = BeautifulSoup(html_melb, 'html.parser')
#melb_soup
melb_containers = melb_soup.find_all('li')

melb_text = []
for line in melb_containers:
    melb_text.append(line.get_text())

melb_study_list = [i for i in melb_text if 'Study name' in i]
melb_study_list = [elem.split("\n") for elem in melb_study_list][1:]
#melb_study_list

sex_melb, age_melb, BMI_melb, weight_melb, med_hist_melb, smoke_hist_melb, status_melb, inpatient_melb, outpatient_melb = [], [], [], [], [], [], [], [], []

for elem in melb_study_list:
    sex_melb.append(elem[0])
    age_melb.append(elem[1])
    BMI_melb.append(elem[2])
    if any('Body Weight' in s for s in elem):
        weight_melb.append([s for s in elem if 'Body Weight' in s])
    else:
        weight_melb.append([""])
    if any('Medical History' in s for s in elem):
        med_hist_melb.append([s for s in elem if 'Medical History' in s])
    else:
        med_hist_melb.append([""])
    smoke_hist_melb.append(elem[5])
    status_melb.append(elem[6])
    inpatient_melb.append(elem[7])
    outpatient_melb.append(elem[8])


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

###---------Age------------
# Standardise age strings
age_melb = [elem.replace('\u202f', ' ') for elem in age_melb]
age_melb = [elem.replace('–', '-') for elem in age_melb]
age_melb = [elem.replace(' ', '') for elem in age_melb]

# Extract min and max ages from string
melb_age = [find_between(elem, 'Age', 'years') for elem in age_melb]
melb_age_min = [elem.split('-')[0] for elem in melb_age]
melb_age_max = [elem.split('-')[1] for elem in melb_age]
#melb_age_min
#melb_age_max

###---------BMI------------
# Standardise BMI strings
BMI_melb = [elem.replace('\u202f', ' ') for elem in BMI_melb]
BMI_melb = [elem.replace('–', '-') for elem in BMI_melb]
BMI_melb = [elem.replace(' ', '') for elem in BMI_melb]

# Extract min and max BMI from string
melb_BMI = [find_between(elem, 'BMI', 'kg') for elem in BMI_melb]
melb_BMI_min = [elem.split('-')[0] for elem in melb_BMI]
melb_BMI_max = [elem.split('-')[1] for elem in melb_BMI]
#melb_BMI_min
#melb_BMI_max

###---------Weight------------
# Flatten list of lists
weight_melb = [item for subl in weight_melb for item in subl]
# Standardise Weight strings
weight_melb = [elem.replace('\u202f', ' ') for elem in weight_melb]
weight_melb = [elem.replace('–', '-') for elem in weight_melb]
# Extract weight requirement from string
melb_weight = [find_between(elem, 'Weight ', 'kg') for elem in weight_melb]
melb_weight
#melb_weight_min = [elem.split('-')[0] for elem in melb_BMI]

###---------Medical History------------
# Flatten list of lists
med_hist_melb = [item for subl in med_hist_melb for item in subl]
# Extract medical history condition
med_hist_melb = [elem.split('History ')[1] for elem in med_hist_melb]
med_hist_melb
