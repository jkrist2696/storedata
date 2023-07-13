# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 03:06:13 2023

@author: jkris
"""

from os import path, getlogin, mkdir
from datetime import datetime
from shutil import copyfile, rmtree
from pandas import read_csv, Series
from time import sleep
from .helper import get_total_ms, format_name, create_dirs, check_live_date, get_date_time
from .helper import create_lockfile, wait_lockfile, delete_lockfile
from .db_backends import db_csv, db_files


def create_run(datapath: str) -> str:
    """Create a directory for a new run in "live" data gathering folder.
    Metadata is saved to the run such as user, date+time, and application name.
    The datapath directory name is taken as the appl name.

    Parameters
    ----------
    datapath : str
        Full path to data storage directory

    Returns
    -------
    rundirpath : str

    """
    _none, applname = path.split(datapath)
    user = getlogin()
    relpaths = ["", "live", "db", "db/daily", "db/artifacts"]
    wait_lockfile(datapath)
    # This could cause an issue if 2 concurrent runs create directories
    create_dirs(datapath, relpaths)
    wait_lockfile(datapath)
    run_update(datapath)
    wait_lockfile(datapath)
    date, time = get_date_time()
    runinfo = {"path": datapath, "date": date, "time": time}
    timepath = path.join(datapath, "live", f"{time}")
    while path.exists(timepath):
        sleep(0.01)
        date, time = get_date_time()
        runinfo = {"path": datapath, "date": date, "time": time}
        timepath = path.join(datapath, "live", f"{time}")
    mkdir(timepath)
    names = ["date_time(yymmdd_ms)", "application", "user"]
    values = [runinfo["date"] + runinfo["time"], applname, user]
    dtypes = ["int", "text", "text"]
    save_data(timepath, names, values, dtypes)
    return timepath


def save_data(runpath: str, names: list[str], values: list, dtypes: list[str]):
    """Save data to a temporary run folder as CSV format.

    Parameters
    ----------
    runpath : str
        Full path to run directory
    names : list[str]
        List of parameters names to save
    values : list
        List of parameters values to save
    dtypes : list[str]
        List of parameters types (dictates saving method)
        Options = [int, float, text/str, blob, file, zip, json]
    """
    wait_lockfile(runpath)
    create_lockfile(runpath, "save_data")
    # dtype options: [int/integer, real/float, text/str, blob, file, zip, json]
    if len(names) != len(values) or len(names) != len(dtypes):
        delete_lockfile(runpath)
        raise RuntimeError("names, values, and dtypes lists must be equal length!")
    # add check for datatypes and existing columns
    parampath = path.join(runpath, "STOREDATA_PARAMS.csv")
    with open(parampath, "a", encoding="ascii") as paramfile:
        for i, name in enumerate(names):
            name = format_name(name, dtypes[i])
            paramfile.write(f"{name},{values[i]}\n")
            if dtypes[i] not in ["file", "blob", "zip"]:
                continue
            _none, filename = path.split(values[i])
            copypath = path.join(runpath, filename)
            copyfile(values[i], copypath)
    delete_lockfile(runpath)
    return parampath


def get_data(datapath: str, names: list[str]):
    """Get data as Pandas DataFrame object from database.

    Parameters
    ----------
    datapath : str
        Full path to data storage directory
    names : list[str]
        Column names to pull from database

    Returns
    -------
    dataframe : Pandas DataFrame
    """
    # convert data back for special dtypes (blob, zip, json)
    dbdirpath = path.join(datapath, "db")
    dbpath = path.join(dbdirpath, "STOREDATA_DB.csv")
    # if path.exists(dbpath):
    dataframe = read_csv(dbpath)
    cols = [col[0 : col.find("[")] for col in dataframe.columns]
    names = [format_name(name, None) for name in names]
    found_names = [
        col
        for name in names
        for i, col in enumerate(dataframe.columns)
        if name.lower() == cols[i].lower()
    ]
    found_inds = [
        j
        for j, name in enumerate(names)
        for i, col in enumerate(dataframe.columns)
        if name.lower() == cols[i].lower()
    ]
    nf_inds = [j for j in range(len(names)) if j not in found_inds]
    nf_names = list(Series(names)[nf_inds])
    if len(nf_names) > 0:
        raise KeyError(
            f"Names ({nf_names}) not found in columns: \n{dataframe.columns}"
        )
    if len(names) == 0:
        return dataframe
    dataframe = dataframe[found_names]
    return dataframe
    # raise KeyError(f"Names ({names}) not found in columns: \n{dataframe.columns}")


def daily_data_to_db(datapath: str):
    """Move all data in "live" folder to the "db" folder by running
    the CSV and Files database backends.

    Parameters
    ----------
    datapath : str
        Full path to data storage directory
    """
    # add conversion of raw files to db based on dtype
    # Copy artifacts
    datepath = path.join(datapath, "live", ".date")
    lastdate = str(check_live_date(datepath))
    db_files(datapath, lastdate)
    # if db is "csv":  , db: str = "csv"
    # Merge all CSVs into dataframe
    db_csv(datapath, lastdate)
    livepath = path.join(datapath, "live")
    rmtree(livepath)
    mkdir(livepath)


def run_update(datapath: str, force: bool = False):
    """Move all data in "live" folder to the "db" folder
    when the ".date" file contains a previous date.

    Parameters
    ----------
    datapath : str
        Full path to data storage directory
    date : int
        YYMMDD formatted date
    force : bool
        True forces the db update even if it is not the next day
    """
    date = int(datetime.now().strftime("%y%m%d"))
    datepath = path.join(datapath, "live", ".date")
    if not path.exists(datepath):
        with open(datepath, "w", encoding="ascii") as datefile:
            datefile.write(f"{date}")
    if (check_live_date(datepath) == date) and (not force):
        return
    create_lockfile(datapath, "daily_data_to_db")
    daily_data_to_db(datapath)
    with open(datepath, "w", encoding="ascii") as datefile:
        datefile.write(f"{date}")
    delete_lockfile(datapath)


# maybe make function for saving and loading runids as json?
