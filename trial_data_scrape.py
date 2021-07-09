import re
import numpy as np
import pandas as pd
from help_funcs import find_between, strip_post_num, strip_pre_colon, total_days
import NZtrials
import nucleus_trials
import cmax_trials


if __name__ == '__main__':
    ###---NZ Trials---
    # Auckland Clinical Trial List URL
    acs_url = 'https://www.clinicalstudies.co.nz/participant-info/current-clinical-trials/'
    # Christchurch Clinical Trial List URL
    ccst_url = 'https://www.ccst.co.nz/study-participants/current-studies/'
    # List must be ordered Auckland then Christchurch
    nz_url_list = [acs_url, ccst_url]
    nz_trials = NZtrials.nz_df(nz_url_list)


    ###---Australia Trials---
    # Melbourne Nucleus Trial List URL
    melb_url = 'https://www.nucleusnetwork.com/au/participate-in-a-trial/melbourne-clinical-trials/'
    # Brisbane Nucleus Trial List URL
    bris_url = 'https://www.nucleusnetwork.com/au/participate-in-a-trial/brisbane-clinical-trials/'
    # Compile url list
    nn_url_list = [melb_url, bris_url]
    # Generate dataframe
    nn_df = nucleus_trials.nucleus_df(nn_url_list)

    # Adelaide Cmax Trial List URL
    cmax_url = 'https://www.cmax.com.au/cmax-current-trials/'
    cmax_df = cmax_trials.cmax_df(cmax_url)

    # Combine all Australian Trials
    aus_trials = nn_df.append(cmax_df, ignore_index = True)
    # Master dataframe
    df = nz_trials.append(aus_trials, ignore_index = True)

    # Formatting
    ## Remove trailing line breaks
    df['eligibility'] = df['eligibility'].replace('(\\n$)','', regex=True)
    df['eligibility'] = df['eligibility'].replace('(\\n$)','', regex=True)
    ## Add bullet point to start of each line
    df['eligibility'] = '• ' + df['eligibility'].replace('(\s?\\n\s*)',' \n• ', regex=True)

    # Check for NAs
    if df.isna().sum().sum() > 0:
        print("NAs found. Check dataframe!")
        print(df.isna().sum())

    # Replace empty string with NaNs
    df = df.replace(r'^\s*$', np.NaN, regex=True)

    df.study_name.fillna("Unknown", inplace=True)
    df.eligibility.fillna("Unknown", inplace=True)
    df.recruiting.fillna(True, inplace=True)
    df.inpatient.fillna(0, inplace=True)
    df.outpatient.fillna(0, inplace=True)
    df.payment.fillna("Unknown", inplace=True)
    df.healthy.fillna(True, inplace=True)
    df.sex_male.fillna(True, inplace=True)
    df.sex_female.fillna(True, inplace=True)
    df.age_min.fillna(18, inplace=True)
    df.age_max.fillna(99, inplace=True)
    df.BMI_min.fillna(16, inplace=True)
    df.BMI_max.fillna(40, inplace=True)
    df.weight_min.fillna(40, inplace=True)
    df.weight_max.fillna(200, inplace=True)

    df.dtypes

    # Convert series type
    df = df.astype(str)

    #df['recruiting'] = pd.to_bool(df['recruiting'], errors='coerce').fillna(True).astype('bool')
    df['inpatient'] = pd.to_numeric(df['inpatient'], errors='coerce').fillna(0).astype('int')
    df['outpatient'] = pd.to_numeric(df['outpatient'], errors='coerce').fillna(0).astype('int')
    df['age_min'] = pd.to_numeric(df['age_min'], errors='coerce').fillna(18).astype('int')
    df['age_max'] = pd.to_numeric(df['age_max'], errors='coerce').fillna(99).astype('int')
    df['BMI_min'] = pd.to_numeric(df['BMI_min'], errors='coerce').fillna(16).astype('int')
    df['BMI_max'] = pd.to_numeric(df['BMI_max'], errors='coerce').fillna(40).astype('int')
    df['weight_min'] = pd.to_numeric(df['weight_min'], errors='coerce').fillna(40).astype('int')
    df['weight_max'] = pd.to_numeric(df['weight_max'], errors='coerce').fillna(200).astype('int')

    df['id'] = df.index

    #df
    # Export to json on Pages
    df.to_json('/Users/danielpetterson/Documents/GitHub/danielpetterson.github.io/assets/trial_data/trial_df.json', orient='records')
    # Subset columns
    df_hist = df[['study_name', 'inpatient', 'outpatient', 'payment', 'city', 'country']]
    # Read in historical file
    df_hist_old = pd.read_json('/Users/danielpetterson/Documents/trial_app_data/trial_hist_df.json')
    # Rowbind and drop later duplicates
    df_hist = pd.concat([df_hist_old,df_hist]).drop_duplicates(keep='first')
    # Save JSON of all trials locally
    df_hist.to_json('/Users/danielpetterson/Documents/trial_app_data/trial_hist_df.json', orient='records')
    print('Success')

#
# import git
#
# repo = git.Repo("/Users/danielpetterson/Documents/GitHub/danielpetterson.github.io/")
#
# repo.config_reader
#
# with repo.config_writer() as git_config:
#     git_config.set_value('user', 'email', 'dpet922@hotmail.com')
#     git_config.set_value('user', 'name', 'danielpetterson')
#
# with repo.config_reader() as git_config:
#     print(git_config.get_value('user', 'email'))
#     print(git_config.get_value('user', 'name'))
#
#     # Reference a remote by its name as part of the object
# print(f'Remote name: {repo.remotes.origin.name}')
# print(f'Remote URL: {repo.remotes.origin.url}')
#
# # Pull from remote repo
# print(repo.remotes.origin.pull())
# # Push changes
# print(repo.remotes.origin.push())
#
# ###---
#
# repo.git.add('--all')
# repo.git.commit('-m', 'commit message from python script')
# origin = repo.remote(name='origin')
# origin.push()
#
#
# PATH_OF_GIT_REPO = r'/Users/danielpetterson/Documents/GitHub/danielpetterson.github.io/'  # make sure .git folder is properly configured
# COMMIT_MESSAGE = 'comment from python script'
#
# def git_push():
#     try:
#         repo = Repo(PATH_OF_GIT_REPO)
#         repo.git.add(update=True)
#         repo.index.commit(COMMIT_MESSAGE)
#         origin = repo.remote(name='origin')
#         origin.push()
#     except:
#         print('Some error occured while pushing the code')
#
# git_push()
#
# ###----
#
