# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 03:44:56 2023

@author: jkris
"""

from re import sub
from os import path, mkdir, remove, getlogin
from time import sleep
from typing import Union
from datetime import datetime
from pandas import concat, DataFrame, read_csv


def get_total_ms(datetime_obj):
    """Get total number of microseconds past in the day from datetime object

    Parameters
    ----------
    datetime_obj :
        datetime object with hour, minute, second, and microsecond properties
    """
    microseconds = (
        datetime_obj.hour * 3600000000
        + datetime_obj.minute * 60000000
        + datetime_obj.second * 1000000
        + datetime_obj.microsecond
    )
    return microseconds


def get_date_time():
    """Get strings for the current date and time.
    The strings can be converted to ints.

    Returns
    -------
    date : str
        format YYMMDD
    time : str
        microseconds
    """
    now = datetime.now()
    date = now.strftime("%y%m%d")
    time = str(get_total_ms(now))
    return date, time


def check_live_date(datepath: str) -> int:
    """Check and return the contents of ".date" file.

    Parameters
    ----------
    datepath : str
        Full path to ".date" file

    Returns
    -------
    lastdate : int
        Date as "YYMMDD" as read from ".date" file

    """
    if not path.exists(datepath):
        return 0
    with open(datepath, "r", encoding="ascii") as datefile:
        lastdate = int(datefile.read())
    return lastdate


def format_name(name: str, dtype: Union[str, None]):
    """Format the name of something by keeping only letters, numbers,
    underscores, and parenthesis.

    Parameters
    ----------
    name : str
        Any string to auto-format into a nicer name
    dtype : Union[str,None]
        Type string to put in brackets after name
    """
    name = sub("[^A-Za-z0-9 _()]+", "", name).lower()
    if dtype:
        name = sub(" ", "_", name) + f"[{dtype}]"
    else:
        name = sub(" ", "_", name)
    return name


def create_dirs(basepath: str, relpaths: list[str]):
    """Create a list of directories after check if each already exists.

    Parameters
    ----------
    basepath : str
        Full path to create the directories in
    relpaths : list[str]
        Relative locations in relation to basepath to make directories
    """
    if not path.exists(basepath):
        mkdir(basepath)
    for relpath in relpaths:
        fullpath = path.join(basepath, relpath)
        if not path.exists(fullpath):
            mkdir(fullpath)


def read_csv_df(csvpath):
    """Read a csv file as a dataframe if the csv path exists.
    Otherwise, output empty dataframe.

    Parameters
    ----------
    csvpath : str
        Full path to csv file

    Returns
    -------
    dataframe : DataFrame
    """
    dataframe = DataFrame()
    if path.exists(csvpath):
        dataframe = read_csv(csvpath)
    return dataframe


def set_or_concat_df(dataframe1, dataframe2):
    """
    Concatenate dataframe2 below dataframe1 if dataframe1 has length greater
    than 0. Otherwise, set dataframe1 equal to dataframe2.
    Parameters
    ----------
    dataframe1 : DataFrame
        Check this df length
    dataframe2 : DataFrame
        Concatenate this df below or use to set equal
    Returns
    -------
    dataframe1 : DataFrame
    """

    if len(dataframe1) == 0:
        dataframe1 = dataframe2
    else:
        dataframe1 = concat([dataframe1, dataframe2], axis=0, ignore_index=False)
    return dataframe1


def create_lockfile(lockdir: str, reason: str):
    """
    Create a ".lock" file in a directory
    Parameters
    ----------
    lockdir : str
        Directory to create lock file in
    reason : str
        Reason for locking directory (written in lock file)
    """
    user = getlogin()
    lockpath = path.join(lockdir, ".lock")
    with open(lockpath, "w", encoding="ascii") as lockfile:
        lockfile.write(f'User "{user}" locking directory for "{reason}".')


def wait_lockfile(lockdir: str, timeout: int = 30):
    """Wait for ".lock" file to be removed at directory.

    Parameters
    ----------
    lockdir : str
        Directory to check for lock file in
    timeout : int
        Maximum time to wait for .lock file to be removed
    """
    lockpath = path.join(lockdir, ".lock")
    for _i in range(timeout):
        if not path.exists(lockpath):
            return
        sleep(1)


def delete_lockfile(lockdir: str):
    """Remove ".lock" file from a directory.

    Parameters
    ----------
    lockdir : str
        Directory to remove lock file from
    """
    lockpath = path.join(lockdir, ".lock")
    if path.exists(lockpath):
        remove(lockpath)
