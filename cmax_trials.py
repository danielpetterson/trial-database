import re
import urllib.request
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

# Remove all text after final digit
def strip_post_num( col ):
    lst = []
    for elem in col.iteritems():
        if (match := re.search('(^.*\d)', elem[1]) is not None):
            lst.append(re.search('(^.*\d)', elem[1]).group(1))
        else:
            lst.append(elem[1])
        col = pd.Series(lst)
    return col

# Remove all text before colon
def strip_pre_colon( col ):
    import re
    lst = []
    for elem in col.iteritems():
        if (match := re.search('(:.*)', elem[1]) is not None):
            string = re.search('(:.*)', elem[1]).group(1)
            string = string.replace(':','').lstrip().replace('x ',' ')
            lst.append(string)
        else:
            lst.append(elem[1].replace('x ',' '))
        col = pd.Series(lst)
    return col

# Calculate total number of days
def total_days( col ):
    lst = []
    for elem in col.iteritems():
        str = elem[1].strip()
        if str == 'None':
            lst.append('0')
        # Checks for numeric value to avoid errors
        if match := re.search('(^.*\d)', str) is not None:
            # Splits on + and carries out any necessary multiplication on either side
            if len(str.split('+')) > 1:
                first = str.split('+')[0].replace('x',' ').strip()
                first = [int(i) for i in first.split()]
                last = str.split('+')[-1].replace('x',' ').strip()
                last = [int(i) for i in last.split()]
                lst.append(np.prod(first)+np.prod(last))
            # Multiplies first and last numbers in string
            elif len(str.split()) > 1:
                lst.append(int(str.split()[0])*int(str.split()[-1]))
            # Appends original number if there is only one inpatient stay
            else:
                lst.append(str)
        else:
            lst.append(str)
        col = pd.Series(lst)
    return col

url = 'https://www.cmax.com.au/cmax-current-trials/'
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, 'html.parser')
soup
study_names = soup.find_all('h2')
study_names_text = []
for line in study_names:
    study_names_text.append(line.get_text())
# Find index of element at start of trial listings
indexes = [idx for idx, s in enumerate(text) if 'CM' in s]
# Isolate study names
study_names = study_names_text[indexes[0]:indexes[-1]]

containers = soup.find_all('span')
text = []
for line in containers:
    text.append(line.get_text())

# Find index of eligibiltity strings
indexes_eligibility = [idx for idx, s in enumerate(text) if 'Eligibility requirements' in s]
indexes_eligibility = [x + 1 for x in indexes_eligibility]
elig_list = [text[i] for i in indexes_eligibility]
elig_list

# Find index of inpatient and outpatient strings
indexes_in_out = [x - 2 for x in indexes_eligibility]
in_out_list = [text[i] for i in indexes_in_out]
in_out_list


def study_info_cmax( study_list ):

    eligibility, recruiting, inpatient, outpatient, payment = [], [], [], [], []
    study_list = [re.sub('( ?)-( ?)|( ?)–( ?)','-',elem) for elem in study_list]
    for elem in study_list:
        eligibility.append(elem)
    study_list = list(map(str.lower,study_list))
    for elem in study_list:
        if (match := re.search('currently recruiting', elem) is not None):
            recruiting.append(True)
        inpatient_str = elem.split('\n')[-3].split('night')[0].strip()
        inpatient.append(inpatient_str)
        outpatient_str = elem.split('\n')[-2].split('visit')[0].strip()
        outpatient.append(outpatient_str)
        payment.append('')

    df = pd.DataFrame(list(zip(eligibility, recruiting, inpatient, outpatient, payment)),
               columns =['eligibility', 'recruiting', 'inpatient', 'outpatient', 'payment'])

    df['inpatient'] = total_days(df['inpatient'])

    return text

study_info_cmax(text)
