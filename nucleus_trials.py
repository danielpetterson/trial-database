import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

html = urllib.request.urlopen('https://www.nucleusnetwork.com/au/participate-in-a-trial/brisbane-clinical-trials/')
soup = BeautifulSoup(html, 'html.parser')
#soup
containers = soup.find_all('li')

text = []
for line in containers:
    text.append(line.get_text())

study_list = [i for i in text if 'Study name' in i]
study_list = [elem.split("\n") for elem in study_list][1:]
#study_list

sex, age, BMI, weight, med_hist, smoke_hist, status, inpatient, outpatient = [], [], [], [], [], [], [], [], []

for elem in study_list:
    sex.append(elem[0])
    age.append(elem[1])
    BMI.append(elem[2])
    if any('Body Weight' in s for s in elem):
        weight.append([s for s in elem if 'Body Weight' in s])
    else:
        weight.append([""])
    if any('Medical History' in s for s in elem):
        med_hist.append([s for s in elem if 'Medical History' in s])
    else:
        med_hist.append([""])
    smoke_hist.append(elem[5])
    status.append(elem[6])
    inpatient.append(elem[7])
    outpatient.append(elem[8])


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

###---------Age------------
# Standardise age strings
age = [elem.replace('\u202f', ' ') for elem in age]
age = [elem.replace('–', '-') for elem in age]
age = [elem.replace(' ', '') for elem in age]

# Extract min and max ages from string
age = [find_between(elem, 'Age', 'years') for elem in age]
age_min = [elem.split('-')[0] for elem in age]
age_max = [elem.split('-')[1] for elem in age]
#age_min
#age_max

###---------BMI------------
# Standardise BMI strings
BMI = [elem.replace('\u202f', ' ') for elem in BMI]
BMI = [elem.replace('–', '-') for elem in BMI]
BMI = [elem.replace(' ', '') for elem in BMI]

# Extract min and max BMI from string
BMI = [find_between(elem, 'BMI', 'kg') for elem in BMI]
BMI_min = [elem.split('-')[0] for elem in BMI]
BMI_max = [elem.split('-')[1] for elem in BMI]
#BMI_min
#BMI_max

###---------Weight------------
# Flatten list of lists
weight = [item for subl in weight for item in subl]
# Standardise Weight strings
weight = [elem.replace('\u202f', ' ') for elem in weight]
weight = [elem.replace('–', '-') for elem in weight]
# Extract weight requirement from string
weight = [find_between(elem, 'Weight ', 'kg') for elem in weight]
weight
#weight_min = [elem.split('-')[0] for elem in BMI]

###---------Medical History------------
# Flatten list of lists
med_hist = [item for subl in med_hist for item in subl]
# Extract medical history condition
med_hist = [elem.split('History ')[1] for elem in med_hist]
med_hist
