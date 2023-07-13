# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 05:08:37 2023

@author: jkris
"""
# %%

from time import sleep
from shutil import rmtree
import sys
from os import path
from importlib import import_module

sys.path.insert(0, path.abspath("../"))
sd = import_module("storedata")

# %%
sys.path.insert(
    0, "C:/Users/jkris/OneDrive/2022_onward/2023/python/myrepo/generic/cleandoc"
)
cd = import_module("cleandoc")
cd.cleandoc_all(
    R"C:\Users\jkris\OneDrive\2022_onward\2023\python\myrepo\generic\storedata\storedata"
)

# %%
for applname in ["appl_name_1", "appl_name_2"]:
    datapath = path.abspath(f"./{applname}")
    if path.exists(datapath):
        rmtree(datapath)
for applname in ["appl_name_1", "appl_name_2"]:
    datapath = path.abspath(f"./{applname}")
    # First day
    names1 = ["col1_as89[-[0SD", "col2_B8232=-", "col3_c3234\\"]
    dtypes = ["int", "text", "file"]
    for i in range(8):
        runpath = sd.create_run(datapath)
        values = [1000, f"i_{i}", "storedata_test.py"]
        csvpath = sd.save_data(runpath, names1, values, dtypes)
    names2 = ["col4_3rj-=QEE", "col2_B8232=-", "col5_09qw8e09"]
    sd.run_update(datapath, force=True)
    sleep(1)
    for i in range(2):
        runpath = sd.create_run(datapath)
        csvpath = sd.save_data(runpath, names2, values, dtypes)
    # Force update
    # run_update(datapath, force = True)
    # First day, additional
    names1 = ["col1_as89[-[0SD", "col2_B8232=-", "col3_c3234\\"]
    dtypes = ["int", "text", "file"]
    for i in range(8):
        runpath = sd.create_run(datapath)
        values = [1000, f"i_{i}", "storedata_test.py"]
        csvpath = sd.save_data(runpath, names1, values, dtypes)
    names2 = ["col4_3rj-=QEE", "col2_B8232=-", "col5_09qw8e09"]
    for i in range(2):
        runpath = sd.create_run(datapath)
        csvpath = sd.save_data(runpath, names2, values, dtypes)
    # Edit date
    # datepath = path.join(datapath,'live','.date')
    # with open(datepath,'w') as datefile:
    #    datefile.write('230708')
    runpath = sd.create_run(datapath)
    csvpath = sd.save_data(runpath, names1, values, dtypes)
    # with open(datepath,'w') as datefile:
    #    datefile.write('230709')
    sd.run_update(datapath, force=True)
    for i in range(3):
        runpath = sd.create_run(datapath)
        csvpath = sd.save_data(runpath, names2, values, dtypes)
    # Get data from database (csv file)
    datadf1 = sd.get_data(datapath, ["col2_B8232=-"])
    print(list(datadf1.iloc[:, 0]))
    datadf2 = sd.get_data(datapath, names1 + ["col4_3rj-=QEE", "col5_09qw8e09"])
    print(datadf2)
    datadf3 = sd.get_data(datapath, [])
    print(datadf3)

# %%
