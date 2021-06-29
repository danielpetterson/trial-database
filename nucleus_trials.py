import urllib.request
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
from help_funcs import find_between, strip_post_num, strip_pre_colon, total_days


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
        df['country'] = 'Australia'

    return df

###---Test---
#nucleus_df(url_list)
