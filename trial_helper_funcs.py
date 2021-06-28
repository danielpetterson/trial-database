import re
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

def total_days( col ):
    lst = []
    for elem in col.iteritems():
        str = elem[1]
        if str == 'None':
            lst.append('0')
        if match := re.search('(^.*\d)', str) is not None:
            if len(str.split()) > 1:
                lst.append(int(str.split()[0])*int(str.split()[-1]))
            else:
                lst.append(str)
        else:
            lst.append(str)
        col = pd.Series(lst)
    return col
