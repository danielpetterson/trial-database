import re
import numpy as np
import pandas as pd
from help_funcs import find_between, strip_post_num, strip_pre_colon, total_days
import NZtrials
import nucleus_trials
import cmax_trials

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

df = nz_trials.append(aus_trials, ignore_index = True)

df.to_csv('trial_df.csv')
# Check for NAs
df.isna().sum()
