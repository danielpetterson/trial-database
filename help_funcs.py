import re
import numpy as np
import pandas as pd

def find_between( string, first, last ):
    try:
        start = string.index( first ) + len( first )
        end = string.index( last, start )
        return string[start:end]
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
    col = col.replace('( ?)x( ?)',' x ', regex=True)
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
