from __future__ import absolute_import, print_function
import os
import re
import sys
from datetime import datetime
import argparse
import numpy as np #to monitor rate cars
import os.path as path
from random import randrange, sample
import math

from data.hail import Hail
from data.driver import Driver
from display import write_data

hails = []
riders = {}
drivers = []
#stores uids of idle drivers
idle_drivers = []
#stores uids of drivers in enroute to rider
enroute_drivers = []
#stores uids of drivers transporting rider
active_drivers = []

def setup_hails(filepath, num_records):
    record = 0
    f = open(filepath, "r")
    entry = f.readline()
    while entry and record < num_records:
        hail_args = []
        entry = entry[entry.find("|")+1:]
        for i in range(0,4):
            bar = entry.find("|")
            hail_args.append(entry[:bar])
            entry = entry[bar+1:]
        hail_args[1] = float(hail_args[1])

        comma = hail_args[2].find(",")
        coord = hail_args[2]
        hail_args[2] = (int(coord[:comma]), int(coord[comma+1:]))

        comma = hail_args[3].find(",")
        coord = hail_args[3]
        hail_args[3] = (int(coord[:comma]), int(coord[comma+1:]))
        #print(hail_args)
        hails.append(Hail(hail_args[0], hail_args[1], hail_args[2], hail_args[3]))
        #print(a_hail)
        #Write your code as a separate module from hailstorm.
        #You can set the location of the output  le like this: 
        #fab -- --outfile="/tmp/hailstorm.out"
        entry = f.readline()
        record += 1
    f.close()
def setup_drivers(dvrs):
    #There are 1000 drivers on the road at any time.
    for i in range(0,1000):
        #drivers with no hails
        drivers.append(Driver(i))
        idle_drivers.append(i)
def dist(x1, x0, y1, y0):
    return math.fabs(x1 - x0) + math.fabs(y1 - y0)

def assign(hailer, time):
    #find closest idle driver
    min_dist = 100000
    min_driver = None

    for idle in idle_drivers:  
        d = drivers[idle]
        distance = dist(hailer.coords_pickup[0], d.coords_curr[0], \
            hailer.coords_pickup[1], d.coords_curr[1])

        if min_dist > distance:
            min_dist = distance
            min_driver = d

    if min_driver != None:
        success = min_driver.attempt_assign(hailer, time)
        if success is True:
            riders[hailer.uid] = hailer
            enroute_drivers.append(min_driver.uid)
            idle_drivers.remove(min_driver.uid)
            return min_driver

    return None

def pickup(curr_time):
    num_pickups = 0
    num_cancels = 0
    sum_time_to_pickup = 0

    for index in enroute_drivers:
        d = drivers[index]
        rider = riders[d.hail_id]
        time_to_pickup = dist(rider.coords_pickup[0], d.coords_curr[0], \
            rider.coords_pickup[1], d.coords_curr[1])
        time_elapsed = curr_time - d.start_time
        #print("time_elapsed is: %d, time_to_pickup is: %d" % (time_elapsed, time_to_pickup))
        if time_elapsed > 30 and time_to_pickup > 30:
            rider = riders.pop(d.hail_id)
            enroute_drivers.remove(d.uid)
            idle_drivers.append(d.uid)
            d.cancel()
            num_cancels += 1
            #print("cancelled")

        elif time_elapsed >= time_to_pickup:
            #start the meter for transporting the rider to dropoff
            d.start_time = curr_time
            enroute_drivers.remove(d.uid)
            active_drivers.append(d.uid)
            num_pickups += 1
            sum_time_to_pickup += time_elapsed

    return num_pickups, num_cancels, sum_time_to_pickup

def dropoff(curr_time):
    num_dropoffs = 0
    for index in active_drivers:
        #check if driver reached rider's destination
        d = drivers[index]
        travelled = curr_time - d.start_time
        if travelled >= d.trip_duration:
            hailer = riders.pop(d.hail_id)
            active_drivers.remove(d.uid)
            idle_drivers.append(d.uid)
            d.drop_off()
            num_dropoffs += 1
            
    return num_dropoffs

def walk(hailer, driver):
    #pickup + dropoff time
    time_driver_travelled = dist(hailer.coords_pickup[0], driver.coords_curr[0], \
        hailer.coords_pickup[1], driver.coords_curr[1]) + \
    dist(hailer.coords_dropoff[0], hailer.coords_pickup[0], \
        hailer.coords_dropoff[1], hailer.coords_pickup[1])

    time_walk = dist(hailer.coords_dropoff[0], hailer.coords_pickup[0], \
        hailer.coords_dropoff[1], hailer.coords_pickup[1])
    time_walk = 20 * time_walk
    #print("%d for hailer %s" % (time_walk, hailer.uid))
    return 1 if time_walk < time_driver_travelled else 0

def dispatch(virtual_time, requested_hails, completed_hails, \
        average_elapsed, walked):
    time = 0

    sum_time_to_pickup = 0
    sum_walkers = 0

    num_requests_made = 0
    num_pickups = 0
    num_cancels = 0
    num_dropoffs = 0

    prev_num_requests_made = 0
    prev_num_pickups = 0
    prev_num_cancels = 0
    prev_num_dropoffs = 0

    while time < virtual_time and len(hails) > 0:
        hailer = hails.pop(0)
        possible_driver = assign(hailer, time)
        if possible_driver:
            num_requests_made += 1
            sum_walkers += walk(hailer, possible_driver)
        else:
            hails.insert(randrange(len(hails)+1), hailer)
        pc = pickup(time)
        num_pickups += pc[0]
        num_cancels += pc[1]
        sum_time_to_pickup += pc[2]

        num_dropoffs += dropoff(time)

        if time%60 == 0:
            requested_hails[time//60] = num_requests_made - prev_num_requests_made
            completed_hails[time//60] = num_dropoffs - prev_num_dropoffs
            if sum_time_to_pickup > 0:
                average_elapsed[time//60] = sum_time_to_pickup/float(num_pickups - prev_num_pickups) 
            if sum_walkers > 0:
                walked[time//60] = sum_walkers/float(num_requests_made - prev_num_requests_made)

            sum_time_to_pickup = 0
            sum_walkers = 0

            prev_num_requests_made = num_requests_made
            prev_num_pickups = num_pickups
            prev_num_cancels = num_cancels
            prev_num_dropoffs = num_dropoffs
            


        time += 1

    #print("num_requests_made %d" % (num_requests_made))
    #print("num_pickups %d" % (num_pickups))
    #print("num_cancels %d" % (num_cancels))
    #print("num_dropoffs %d" % (num_dropoffs))

def run():

    parser = argparse.ArgumentParser(description="Simulate Uber")
    parser.add_argument("--source/","--source/", help="filepath to read in hails", required=True)
    parser.add_argument("--num-records","--num-records", help="number of hails to process", required=True)
    args = vars(parser.parse_args())

    for k, v in args.items():
        print("{k} = {v}".format(k=k, v=v))

    setup_drivers(drivers)
    setup_hails(args["source/"], int(args["num_records"]))


    virtual_day = 3
    #keep at order of minutes so can match up to blocks
    virtual_time = virtual_day*24*60
    #virtual_time = 100

    #hails requested per hr
    requested_hails = np.zeros(virtual_time//60)
    #hails completed per hr
    completed_hails = np.zeros(virtual_time//60)
    #average time elapsed between hailing and pickup per hr
    average_elapsed = np.zeros(virtual_time//60)
    #percentage of riders who would have arrived at their
    #destination sooner if they had walked, for each hr of the run
    walked = np.zeros(virtual_time//60)
    dispatch(virtual_time, requested_hails, completed_hails, \
        average_elapsed, walked)

    write_data(virtual_time//60, requested_hails, completed_hails, average_elapsed, walked)


if __name__ == "__main__": 
    run()
