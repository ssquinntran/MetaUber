from __future__ import absolute_import, print_function
import csv
import numpy as np
from tabulate import tabulate

def write_data(total_hrs, requested_hails, completed_hails, \
    average_elapsed, walked):
    f = open("../../output.txt", "w")

    f.write("hails per hour, for each hour of the run, " \
        "both requested and completed\n")
    table = []
    for hr in range(0, total_hrs):
        table.append([hr, requested_hails[hr], completed_hails[hr]])
    f.write(tabulate(table,headers=["HOUR","REQUESTED", "COMPLETED"]))

    f.write("\naverage time elapsed between hailing and pickup," \
        " for each hour of the run\n")
    table = []
    for hr in range(0, total_hrs):
        table.append([hr, average_elapsed[hr]])
    f.write(tabulate(table,headers=["HOUR","AVERAGE ELAPSED TIME"]))

    f.write("\npercentage of riders who would have arrived at" \
        "their destination sooner if they had walked, " \
        "for each hour of the run\n")
    table = []
    for hr in range(0, total_hrs):
        table.append([hr, walked[hr]])
    f.write(tabulate(table,headers=["HOUR","PERCENTAGE"]))


    f.close()