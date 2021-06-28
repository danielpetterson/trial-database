import urllib.request
from bs4 import BeautifulSoup
import re
import pandas as pd

html = urllib.request.urlopen('https://www.nucleusnetwork.com/au/participate-in-a-trial/melbourne-clinical-trials/')
soup = BeautifulSoup(html, 'html.parser')
containers = soup.find_all('li')
text = []
for line in containers:
    text.append(line.get_text())
# Extract relevant lines minus header
study_list = [i for i in text if 'Study name' in i][1:]

study_list

def nucleus_df( html ):
    soup = BeautifulSoup(html, 'html.parser')
    containers = soup.find_all('li')
    text = []
    for line in containers:
        text.append(line.get_text())
    # Extract relevant lines minus header
    study_list = [i for i in text if 'Study name' in i][1:]
    study_name, eligibility, status, inpatient, outpatient, payment, city = [], [], [], [], [], [], []
    study_list = [re.sub('( ?)-( ?)|( ?)–( ?)','-',elem) for elem in study_list]
    study_list = list(map(str.lower,study_list))
    for elem in study_list:
        healthy.append(any(substring in elem for substring in ['healthy']))
        if (match := re.search('(^| )male', elem) is not None):
            sex_male.append(True)
        if (match := re.search('(^| )female', elem) is not None):
            sex_female.append(True)
        elem_age_range = elem.split('\n')[1].split('age ')[1].split('years')[0].split('-')
        age_min.append(elem_age_range[0])
        if len(elem_age_range) > 1:
            age_max.append(elem_age_range[-1])
        else:
            age_max.append('')
        elem_bmi = elem.split('\n')[2].split(' kg/m')[0]
        if 'bmi' in elem_bmi:
            bmi_range = elem_bmi.split(' ')[-1].split('-')
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

nucleus_df(html)

study_list

def study_info_nucleus( study_list ):

    study_name, eligibility, recruiting, inpatient, outpatient, payment, city = [], [], [], [], [], [], []
    study_list = [re.sub('( ?)-( ?)|( ?)–( ?)','-',elem) for elem in study_list]
    study_list = list(map(str.lower,study_list))
    for elem in study_list:
        study_name.append(find_between(elem.split('\n')[0], 'study name ', ' study').capitalize())
        eligibility.append(elem)
        if (match := re.search('currently recruiting', elem) is not None):
            recruiting.append(True)
    #
    #
    #     if (match := re.search('(^| )male', elem) is not None):
    #         sex_male.append(True)
    #     if (match := re.search('(^| )female', elem) is not None):
    #         sex_female.append(True)
    #     elem_age_range = elem.split('\n')[1].split('age ')[1].split('years')[0].split('-')
    #     age_min.append(elem_age_range[0])
    #     if len(elem_age_range) > 1:
    #         age_max.append(elem_age_range[-1])
    #     else:
    #         age_max.append('')
    #     elem_bmi = elem.split('\n')[2].split(' kg/m')[0]
    #     if 'bmi' in elem_bmi:
    #         bmi_range = elem_bmi.split(' ')[-1].split('-')
    #         BMI_min.append(bmi_range[0])
    #         if len(bmi_range) > 1:
    #             BMI_max.append(bmi_range[-1])
    #         else:
    #             BMI_max.append('')
    #     else:
    #         BMI_min.append('')
    #         BMI_max.append('')
    #     if 'weight' in elem:
    #         elem_weight_range = find_between(elem, 'weight', 'kg').replace('>','').strip().split('-')#[-1].split('-')
    #         weight_min.append(elem_weight_range[0])
    #         if len(elem_weight_range) > 1:
    #             weight_max.append(elem_weight_range[-1])
    #         else:
    #             weight_max.append('')
    #     else:
    #         weight_min.append('')
    #         weight_max.append('')
    #
    # df = pd.DataFrame(list(zip(healthy, sex_male, sex_female, age_min, age_max, BMI_min, BMI_max, weight_min, weight_max)),
    #            columns =['healthy', 'sex_male', 'sex_female', 'age_min', 'age_max', 'BMI_min', 'BMI_max', 'weight_min', 'weight_max'])
    #
    return recruiting

study_info_nucleus(study_list)

def requirements( study_list ):
    healthy, sex_male, sex_female, age_min, age_max, BMI_min, BMI_max, weight_min, weight_max = [], [], [], [], [], [], [], [], []
    study_list = [re.sub('( ?)-( ?)|( ?)–( ?)','-',elem) for elem in study_list]
    study_list = list(map(str.lower,study_list))
    for elem in study_list:
        healthy.append(any(substring in elem for substring in ['healthy']))
        if (match := re.search('(^| )male', elem) is not None):
            sex_male.append(True)
        if (match := re.search('(^| )female', elem) is not None):
            sex_female.append(True)
        elem_age_range = elem.split('\n')[1].split('age ')[1].split('years')[0].split('-')
        age_min.append(elem_age_range[0])
        if len(elem_age_range) > 1:
            age_max.append(elem_age_range[-1])
        else:
            age_max.append('')
        elem_bmi = elem.split('\n')[2].split(' kg/m')[0]
        if 'bmi' in elem_bmi:
            bmi_range = elem_bmi.split(' ')[-1].split('-')
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
