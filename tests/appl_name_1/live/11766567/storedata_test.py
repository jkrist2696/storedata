# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 05:08:37 2023

@author: jkris
"""

from os import path
from shutil import rmtree
import sys
sys.path.insert(0,path.abspath("../"))
from storedata import create_run, save_data, get_data

sys.path.insert(0,'C:/Users/jkris/OneDrive/2022_onward/2023/python/myrepo/generic/cleandoc')
from cleandoc import cleandoc_all

cleandoc_all(R"C:\Users\jkris\OneDrive\2022_onward\2023\python\myrepo\generic\storedata\storedata")


for applname in ["appl_name_1","appl_name_2"]:
    datapath = path.abspath(f"./{applname}")
    if path.exists(datapath):
        rmtree(datapath)
    names1 = ["col1_as89[-[0SD", "col2_B8232=-", "col3_c3234\\"]
    dtypes = ["int", "text", "file"]
    for i in range(8):
        runpath = create_run(datapath)
        values = [1000, f"i_{i}", "storedata_test.py"]
        csvpath = save_data(runpath, names1, values, dtypes)
    names2 = ["col4_3rj-=\QEE", "col2_B8232=-", "col5_09qw8e09"]
    for i in range(2):
        runpath = create_run(datapath)
        csvpath = save_data(runpath, names2, values, dtypes)
    # Edit date
    datepath = path.join(datapath,'live','.date')
    with open(datepath,'w') as datefile:
        datefile.write('230708')
    runpath = create_run(datapath)
    csvpath = save_data(runpath, names1, values, dtypes)
    with open(datepath,'w') as datefile:
        datefile.write('230709')
    for i in range(3):
        runpath = create_run(datapath)
        csvpath = save_data(runpath, names2, values, dtypes)
    # replace below with get_data
    datadf1 = get_data(datapath, ["col2_B8232=-"])
    print(list(datadf1.iloc[:,0]))
    datadf2 = get_data(datapath, names1+["col4_3rj-=\QEE","col5_09qw8e09"])
    print(datadf2)
    datadf3 = get_data(datapath, [])
    print(datadf3)
