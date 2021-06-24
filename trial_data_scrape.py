import pandas as pd
import re
import urllib.request
from bs4 import BeautifulSoup
from html_table_parser.parser import HTMLTableParser

def url_get_contents(url):

    #making request to the website
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)

    #reading contents of the website
    return f.read()


###---------------------- NZ DataFrame -----------------------------
# defining the html contents of a URL.
xhtml_acs = url_get_contents('https://www.clinicalstudies.co.nz/participant-info/current-clinical-trials/').decode('utf-8')
xhtml_ccst = url_get_contents('https://www.ccst.co.nz/study-participants/current-studies/').decode('utf-8')
# Defining the HTMLTableParser object
parser = HTMLTableParser()

# feeding the html contents in the
# HTMLTableParser object
parser.feed(xhtml_acs)
parser.feed(xhtml_ccst)

# Now finally obtaining the data of
# the table required
acs_table_list = parser.tables[0][1:]
ccst_table_list = parser.tables[1][1:]
header = ('study_name', 'eligibility', 'status', 'inpatient', 'outpatient', 'payment')
acs_df = pd.DataFrame(acs_table_list).drop(6, axis=1)
acs_df.columns = header
acs_df['city'] = 'Auckland'

ccst_df = pd.DataFrame(ccst_table_list, columns = parser.tables[1][0])

ccst_df['inpatient'] = ccst_df['Study Visits'][ccst_df['Study Visits'].str.contains('night')]
ccst_df['inpatient'].fillna('',inplace=True)
ccst_df['inpatient'] = [val[0] for val in ccst_df['inpatient'].str.split('(\+|and)')]

ccst_df['outpatient'] = [val[-1] for val in ccst_df['Study Visits'].str.split('(\+|and)')]
ccst_df['outpatient'] = ccst_df['outpatient'].str.extract('((\d*\-\d)|(\d))')[0]

ccst_df['payment'] = ccst_df['Reimbursement']

ccst_df.drop(['Dates', 'Study Visits', 'Reimbursement'], axis=1, inplace=True)
ccst_df.columns = header
ccst_df['city'] = 'Christchurch'

# Check resulting dataframes
#ccst_df
#acs_df

nz_df = pd.concat([acs_df,ccst_df], ignore_index=True)

nz_df['study_name']=[val[0] for val in nz_df['study_name'].str.split(' ')]
nz_df['study_name']=[val for val in nz_df['study_name'].str.capitalize()]
nz_df


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
    med_hist_melb.append(elem[4])
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
weight_melb
# Extract min and max BMI from string
melb_weight = [find_between(elem, 'Weight ', 'kg') for elem in weight_melb]
melb_weight
#melb_weight_min = [elem.split('-')[0] for elem in melb_BMI]
#melb_BMI_max = [elem.split('-')[1] for elem in melb_BMI]
#melb_BMI_min
#melb_BMI_max
