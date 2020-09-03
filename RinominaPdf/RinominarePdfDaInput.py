import ctypes
import PyPDF2
import shlex
import os
from progressbar import ProgressBar
from datetime import date

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

pbar = ProgressBar()
df = pd.read_excel('rinomina.xlsx')

#print("Column headings:")
#print(df.columns)
#print("\n\nStampa colonna1")
#print(df['old'])

for i,j in df['old'].iteritems():
    old = df['old'][i]
    new = df['nuovo'][i]
    old_name = old
    new_name = new
    os.rename(old_name, new_name)
