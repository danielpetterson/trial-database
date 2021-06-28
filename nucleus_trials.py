import urllib.request
from bs4 import BeautifulSoup
import re
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



def study_info_nucleus( study_list ):

    study_name, eligibility, recruiting, inpatient, outpatient, payment = [], [], [], [], [], []
    study_list = [re.sub('( ?)-( ?)|( ?)–( ?)','-',elem) for elem in study_list]
    for elem in study_list:
        eligibility.append(elem.split('Eligibility')[1])
    study_list = list(map(str.lower,study_list))
    for elem in study_list:
        study_name.append(find_between(elem.split('\n')[0], 'study name ', ' study').capitalize())
        if (match := re.search('currently recruiting', elem) is not None):
            recruiting.append(True)
        inpatient_str = elem.split('\n')[-3].split('night')[0].strip()
        inpatient.append(inpatient_str)
        outpatient_str = elem.split('\n')[-2].split('visit')[0].strip()
        outpatient.append(outpatient_str)
        payment.append('')

    df = pd.DataFrame(list(zip(study_name, eligibility, recruiting, inpatient, outpatient, payment)),
               columns =['study_name', 'eligibility', 'recruiting', 'inpatient', 'outpatient', 'payment'])

    df['inpatient'] = total_days(df['inpatient'])

    return df

study_info_nucleus(study_list)

def requirements( study_list ):
    healthy, sex_male, sex_female, age_min, age_max, BMI_min, BMI_max, weight_min, weight_max = [], [], [], [], [], [], [], [], []
    study_list = [re.sub('( ?)-( ?)|( ?)–( ?)','-',elem) for elem in study_list]
    study_list = [re.sub('\u202f','',elem) for elem in study_list]
    study_list = list(map(str.lower,study_list))
    for elem in study_list:
        healthy.append(any(substring in elem for substring in ['healthy']))
        if (match := re.search('(^| )male', elem) is not None):
            sex_male.append(True)
        if (match := re.search('(^| )female', elem) is not None):
            sex_female.append(True)
        elem_age_range = elem.split('age ')[1].split('years')[0].strip().split('-')
        age_min.append(elem_age_range[0])
        if len(elem_age_range) > 1:
            age_max.append(elem_age_range[-1])
        else:
            age_max.append('')
        if 'bmi' in elem:
            bmi_range = find_between(elem, 'bmi', 'kg').strip().split('-')
            BMI_min.append(bmi_range[0])
            if len(bmi_range) > 1:
                BMI_max.append(bmi_range[-1])
            else:
                BMI_max.append('')
        else:
            BMI_min.append('')
            BMI_max.append('')
        if 'weight' in elem:
            elem_weight_range = find_between(elem, 'weight', 'kg').replace('>','').strip().split('-')#[-1].split('-')
            weight_min.append(elem_weight_range[0])
            if len(elem_weight_range) > 1:
                weight_max.append(elem_weight_range[-1])
            else:
                weight_max.append('')
        else:
            weight_min.append('')
            weight_max.append('')

    df = pd.DataFrame(list(zip(healthy, sex_male, sex_female, age_min, age_max, BMI_min, BMI_max, weight_min, weight_max)),
               columns =['healthy', 'sex_male', 'sex_female', 'age_min', 'age_max', 'BMI_min', 'BMI_max', 'weight_min', 'weight_max'])


    return df

requirements(study_list)


# Melbourne Nucleus Trial List URL
melb_url = 'https://www.nucleusnetwork.com/au/participate-in-a-trial/melbourne-clinical-trials/'
# Brisbane Nucleus Trial List URL
bris_url = 'https://www.nucleusnetwork.com/au/participate-in-a-trial/brisbane-clinical-trials/'

url_list = [melb_url, bris_url]

def nucleus_df( url_list ):
    df = pd.DataFrame(columns =['study_name', 'eligibility', 'recruiting', 'inpatient', 'outpatient', 'payment', 'healthy', 'sex_male', 'sex_female', 'age_min', 'age_max', 'BMI_min', 'BMI_max', 'weight_min', 'weight_max'])
    for url in url_list:
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        containers = soup.find_all('li')
        text = []
        for line in containers:
            text.append(line.get_text())
        # Extract relevant lines minus header
        study_lines = [i for i in text if 'Study name' in i][1:]
        study_info = study_info_nucleus(study_lines)
        study_requirements = requirements(study_lines)
        if 'melbourne' in url:
            study_info['city'] = 'Melbourne'
            df = pd.concat([study_info, study_requirements], axis=1)
        else:
            study_info['city'] = 'Brisbane'
            df_bris = pd.concat([study_info, study_requirements], axis=1)
            df = df.append(df_bris, ignore_index = True)

    return df

nucleus_df(url_list)
