import re
import urllib.request
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from help_funcs import find_between, strip_post_num, strip_pre_colon, total_days

url = 'https://www.cmax.com.au/cmax-current-trials/'

def study_info_cmax( url ):

    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    # Initialise dataframe
    df = pd.DataFrame()
    # Find h2 elements for study names
    study_names = soup.find_all('h2')
    study_names_text = []
    for line in study_names:
        study_names_text.append(line.get_text())
    # Find index of element at start of trial listings
    indexes = [idx for idx, s in enumerate(study_names_text) if 'CM' in s]
    # Isolate study names and append column to df
    df['study_names'] = study_names_text[indexes[0]:]

    # Find all span elements for further study details and requirements
    containers = soup.find_all('span')
    text = []
    for line in containers:
        text.append(line.get_text())

    # Find index of eligibiltity strings
    indexes_eligibility = [idx for idx, s in enumerate(text) if 'Eligibility requirements' in s]
    indexes_eligibility = [x + 1 for x in indexes_eligibility]
    elig_list = [text[i] for i in indexes_eligibility]
    elig_list = [re.sub('\n\n',' ',elem) for elem in elig_list]
    df['eligibility'] = elig_list
    df['recruiting'] = True

    ###---Inpatient and outpatient duration---
    # Find index of inpatient and outpatient strings
    indexes_in_out = [x - 2 for x in indexes_eligibility]
    in_out_list = [text[i] for i in indexes_in_out]
    outpatient = []
    inpatient = []
    # Formatting strings
    in_out_list = [re.sub('( ?)-( ?)|( ?)–( ?)','-',elem) for elem in in_out_list]
    in_out_list = [elem.lower() for elem in in_out_list]

    for elem in in_out_list:
        if (match := re.search('night', elem) is not None):
            in_elem = elem.split(')')[0].split('night')[0].strip()
            if (match := re.search('\+', in_elem) is not None) and (match := re.search('\(', in_elem) is not None):
                in_elem_brac = in_elem.split('(')[-1]
                inpatient.append(in_elem_brac)
            elif (match := re.search('\(', in_elem) is not None) and (match := re.search('\+', in_elem) is None):
                in_elem = re.sub('\(','',in_elem)
                in_elem_mult = in_elem.split()
                if len(in_elem_mult) > 1:
                    in_elem_mult = " x ".join([in_elem_mult[0],in_elem_mult[-1]])
                    inpatient.append(in_elem_mult)
                else:
                    inpatient.append(in_elem_mult[0])
            else:
                inpatient.append(in_elem)
        else:
            inpatient.append('0')
        out = elem.split('night')[-1].split('visit')[0].split('+')[-1].strip()
        if (match := re.search('visit', elem) is not None):
            outpatient.append(out)
        else:
            outpatient.append('0')
    # Append columns
    df['inpatient'] = inpatient
    df['outpatient'] = outpatient

    # Calculate total total_days
    df['inpatient'] = df['inpatient'].replace('( ?)x( ?)',' x ', regex=True)
    df['inpatient'] = total_days(df['inpatient'])
    df['outpatient'] = df['outpatient'].replace('( ?)x( ?)',' x ', regex=True)
    df['outpatient'] = total_days(df['outpatient'])

    ###---Payment Amount---
    # Extract hyperlinks to pages containing payment amount
    href = soup.find_all('a')
    href_index = [idx for idx, s in enumerate(href) if 'Read More' in s]
    link_list = href[href_index[0]:(href_index[-1]+1)]

    links = []
    for elem in link_list:
        link = str(elem).split('"')[1]
        links.append(link)

    payment = []
    for elem in links:

        html_payment = urllib.request.urlopen(elem)
        link_soup = BeautifulSoup(html_payment, 'html.parser').find('body')
        pars = link_soup.find_all(['p', 'div'])
        pars_text = []
        for line in pars:
            pars_text.append(line.get_text())
        payment_index = [idx for idx, s in enumerate(pars_text) if '$' in s]
        payment_str = str(pars[payment_index[0]])
        payment_amount = help_funcs.find_between(payment_str, '$', ' t').strip().split('<')[0]
        payment.append(payment_amount)

    df['payment'] = payment
    df['payment'] = df['payment'].replace(',|\$| ','', regex=True)

    ###---Geographic Info---
    df['city'] = 'Adelaide'
    df['country'] = 'Australia'

    return df


def requirements( eligibility_col ):
    healthy, sex_male, sex_female, age_min, age_max, BMI_min, BMI_max, weight_min, weight_max = [], [], [], [], [], [], [], [], []
    for elem in eligibility_col:
        elem = elem.lower()
        healthy.append(any(substring in elem for substring in ['healthy', 'good general health']))
        if (match := re.search('(^| )male', elem) is not None) and (match := re.search('(^| )female', elem) is not None):
            sex_male.append(True)
            sex_female.append(True)
        elif (match := re.search('(^| )male', elem) is not None):
            sex_male.append(True)
            sex_female.append(False)
        elif (match := re.search('(^| )female', elem) is not None):
            sex_male.append(False)
            sex_female.append(True)
        elem_age_range = elem.split('year')[0]
        age_min_str = elem_age_range.split(' to ')[0].split(' ')[-1]
        age_min.append(age_min_str)
        if len(elem_age_range) > 1:
            age_max.append(elem_age_range.split(' to ')[-1])
        else:
            age_max.append('')
        elem_bmi = elem.split('kg/m')[0].rstrip()
        bmi_range = elem_bmi.split('between')[-1].split('below')[-1].strip()
        if 'bmi' in elem_bmi:
            BMI_min.append(bmi_range.split(' to ')[0])
            if len(bmi_range) > 1:
                BMI_max.append(bmi_range.split(' to ')[-1])
            else:
                BMI_max.append('')
        else:
            BMI_min.append('')
            BMI_max.append('')
        if 'weigh' in elem:
            elem_weight_range = find_between(elem, 'weigh', 'kg')
            if (match := re.search('above', elem_weight_range) is not None) or (match := re.search('least', elem_weight_range) is not None):
                weight_min.append(elem_weight_range.split('above')[-1].split('least')[-1])
                weight_max.append('')
            else:
                weight_min.append(elem_weight_range.split(" to ")[0].strip().split()[-1])
                weight_max.append(elem_weight_range.split(" to ")[-1].strip().split()[-1])
        else:
            weight_min.append('')
            weight_max.append('')

    df = pd.DataFrame(list(zip(healthy, sex_male, sex_female, age_min, age_max, BMI_min, BMI_max, weight_min, weight_max)),
               columns =['healthy', 'sex_male', 'sex_female', 'age_min', 'age_max', 'BMI_min', 'BMI_max', 'weight_min', 'weight_max'])

    # Replace minimum BMI with empty string if max and min are the same.
    df.loc[df['BMI_min'].eq(df['BMI_max']), 'BMI_min'] = ''
    # Replace max weight with empty string if max and min are the same.
    df.loc[df['weight_min'].eq(df['weight_max']), 'weight_max'] = ''

    return df

def cmax_df( url ):

    study_info = study_info_cmax(url)
    study_requirements = requirements(study_info.eligibility)
    df = pd.concat([study_info, study_requirements], axis=1)

    return df

#cmax_df(url)
