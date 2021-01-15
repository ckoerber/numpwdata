"""Utility functions related to parsing files."""
import re

from numpy import array
from pandas import DataFrame


def parse_fortran_funny(string):
    """Convert fortran format arrys in file to python objects."""
    for pat, subs in {
        f"{key}*{val}": ", ".join([val] * int(key))
        for key, val in set(
            re.findall(r"([0-9]+)\*([\-0-9]+)", re.sub(r"\s+", " ", string))
        )
    }.items():
        string = string.replace(pat, subs)

    arr = array(list(map(int, string.split(","))))
    nd = len(arr) // 8
    return DataFrame(
        data=arr.reshape([nd, 8]),
        columns=[
            "ms3_x2",
            "mt3_x2",
            "mjtot_x2",
            "ms3p_x2",
            "mt3p_x2",
            "mjtotp_x2",
            "k",
            "bk",
        ],
    )
