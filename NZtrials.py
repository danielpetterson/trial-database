import re
import pandas as pd
from trial_helper_funcs import find_between, strip_post_num, strip_pre_colon, total_days

###---Auckland---
# Read in ACS table
acs_df = pd.read_html('https://www.clinicalstudies.co.nz/participant-info/current-clinical-trials/')[0]
acs_df.drop("Group Timetables", axis=1, inplace=True)
# Rename columns and append city
header = ('study_name', 'eligibility', 'status', 'inpatient', 'outpatient', 'payment')
acs_df.columns = header
acs_df['city'] = 'Auckland'

###---Christchurch---
# Read in Chch table
ccst_df = pd.read_html('https://www.ccst.co.nz/study-participants/current-studies/',header=0)[0]
# Extract number of inpatient days
ccst_df['inpatient'] = ccst_df['Study Visits'][ccst_df['Study Visits'].str.contains('night')]
ccst_df['inpatient'].fillna('None',inplace=True)
ccst_df['inpatient'] = [val[0] for val in ccst_df['inpatient'].str.split('(\+|and)')]
# Extract number of outpatient days
ccst_df['outpatient'] = [val[-1] for val in ccst_df['Study Visits'].str.split('(\+|and)')]
ccst_df['outpatient'] = ccst_df['outpatient'].str.extract('((\d*\-\d)|(\d))')[0]
# Rename reimbursement column
ccst_df['payment'] = ccst_df['Reimbursement']
# Drop excess columns
ccst_df.drop(['Dates', 'Study Visits', 'Reimbursement'], axis=1, inplace=True)
# Rename columns to align with Auckland layout
ccst_df.columns = header
# Append city
ccst_df['city'] = 'Christchurch'

# Check resulting dataframes
#ccst_df
#acs_df

# Rowbind dataframes
nz_df = pd.concat([acs_df,ccst_df], ignore_index=True)
# Standardise study names
nz_df['study_name']=[val[0] for val in nz_df['study_name'].str.split(' ')]
nz_df['study_name']=[val for val in nz_df['study_name'].str.capitalize()]

nz_df = nz_df.replace('( ?)-( ?)|( ?)–( ?)','-', regex=True)
nz_df['eligibility'] = nz_df['eligibility'].str.lower().replace('(^| )women ',' females ', regex=True).replace('(^| )men ',' males ', regex=True)

nz_df['payment'] = [re.search('(\$.*\d)', elem).group(1) for elem in nz_df['payment']]

nz_df['payment'] = [elem.replace('NZ ', '') for elem in nz_df['payment']]
nz_df['payment'] = [elem.replace('(\.*\:)', '') for elem in nz_df['payment']]
nz_df['payment'] = [re.sub('( .*:)', ' - ', elem) for elem in nz_df['payment']]
nz_df['payment'] = nz_df['payment'].replace('\$|, |,|\.00','', regex=True)

to_sub = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'none': '0'
}

nz_df['inpatient']=[val for val in nz_df['inpatient'].str.lower()]
nz_df['outpatient']=[val for val in nz_df['outpatient'].str.lower()]
nz_df['inpatient'] = nz_df['inpatient'].apply(lambda x: ' '.join([to_sub.get(i, i) for i in x.split()]))


nz_df['inpatient'] = strip_post_num(nz_df['inpatient'])
nz_df['inpatient'] = strip_pre_colon(nz_df['inpatient'])
nz_df['inpatient'] = total_days(nz_df['inpatient'])

nz_df['outpatient'] = strip_post_num(nz_df['outpatient'])
nz_df['outpatient'] = strip_pre_colon(nz_df['outpatient'])

nz_df['status'] = nz_df['status'].str.contains('currently recruiting', case=False)
nz_df.rename(columns = {'status':'recruiting'}, inplace = True)

nz_df



def requirements( eligibility_col ):
    healthy, sex_male, sex_female, age_min, age_max, BMI_min, BMI_max, weight_min, weight_max = [], [], [], [], [], [], [], [], []
    for elem in eligibility_col:
        elem = elem.lower()
        healthy.append(any(substring in elem for substring in ['healthy', 'good health']))
        if (match := re.search('(^| )male', elem) is not None):
            sex_male.append(True)
        if (match := re.search('(^| )female', elem) is not None):
            sex_female.append(True)
        elem_age_range = elem.split('year')[0].split('weight')[0].split('aged ')[1].split(' ')[0].split('-')
        age_min.append(elem_age_range[0])
        if len(elem_age_range) > 1:
            age_max.append(elem_age_range[-1])
        else:
            age_max.append('')
        elem_bmi = elem.split('kg/m')[0].rstrip()
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
        if 'weigh' in elem:
            elem_weight_range = find_between(elem, 'weigh', 'kg').rstrip().split(' ')[-1].replace('>','').split('-')
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

requirements(nz_df['eligibility'])