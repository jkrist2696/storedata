# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 13:39:55 2023

@author: jkris
"""

from os import listdir, path, mkdir
from shutil import copyfile
from pandas import DataFrame, read_csv, concat

# with ZipFile('spam.zip','w') as myzip:
#     with myzip.open('eggs.txt','w') as myfile:
#         myfile.write(b'test writing zip')


def db_csv(datapath: str, date: str):
    """Move parameters in temporary data storage for each run to a
    database stored as a CSV file.

    Parameters
    ----------
    datapath : str
        Full path to data storage
    date : str
        YYMMDD formatted date
    """
    livepath, dbdirpath, dailypath = get_db_paths(datapath)[0:3]
    dbdailypath = path.join(dailypath, f"STOREDATA_{date}.csv")
    if path.exists(dbdailypath):
        df_daily = read_csv(dbdailypath)
    else:
        df_daily = DataFrame()
    for dirname in listdir(livepath):
        if not path.isdir(path.join(livepath, dirname)):
            continue
        parampath = path.join(livepath, dirname, "STOREDATA_PARAMS.csv")
        df_run = read_csv(parampath, index_col=0, header=None).T
        if len(df_daily) == 0:
            df_daily = df_run
        else:
            df_daily = concat([df_daily, df_run], axis=0, ignore_index=False)

    df_daily.to_csv(dbdailypath, index=False, na_rep="NaN")
    # Make below a separate function
    dbpath = path.join(dbdirpath, "STOREDATA_DB.csv")
    if path.exists(dbpath):
        df_db = read_csv(dbpath)
        df_db = concat([df_db, df_daily], axis=0, ignore_index=False)
    else:
        df_db = df_daily
    df_db.to_csv(dbpath, index=False, na_rep="NaN")
    # Add code here to make a backup of db if merge is successful


def db_files(datapath: str, date: str):
    """Move parameters in temporary data storage for each run to a
    cataloged files folder.

    Parameters
    ----------
    datapath : str
        Full path to data storage
    date : str
        YYMMDD formatted data
    """
    livepath, _none, _none, artpath = get_db_paths(datapath)
    dateartpath = path.join(artpath, date)
    if not path.exists(dateartpath):
        mkdir(dateartpath)
    for timedir in listdir(livepath):
        rundir = path.join(livepath, timedir)
        if not path.isdir(rundir):
            continue
        mkdir(path.join(dateartpath, timedir))
        parampath = path.join(rundir, "STOREDATA_PARAMS.csv")
        df_run = read_csv(parampath, index_col=0, header=None).T
        for colname in df_run.columns:
            if "[file]" in colname:
                value = df_run.loc[1, colname]
                _none, filename = path.split(value)
                oldpath = path.join(rundir, filename)
                newpath = path.join(dateartpath, timedir, filename)
                copyfile(oldpath, newpath)
                df_run[colname] = newpath
            elif "[zip]" in colname:
                # insert zip logic here
                pass
        df_run.T.to_csv(parampath, header=False)


def get_db_paths(datapath: str):
    """Get many important nested paths in DB to save lines from many path.joins

    Parameters
    ----------
    datapath : str
        Full path to data storage directory
    """
    livepath = path.join(datapath, "live")
    dbdirpath = path.join(datapath, "db")
    dailypath = path.join(datapath, "db", "daily")
    artpath = path.join(datapath, "db", "artifacts")
    return livepath, dbdirpath, dailypath, artpath
