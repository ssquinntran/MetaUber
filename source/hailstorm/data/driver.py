from __future__ import absolute_import
import random
import time
import uuid
import math

RANGE_GRID = (0,99)
"""
Drivers travel at a speed of 60 blocks/hr.
The maximum amount of time a rider is willing to wait for their driver to pick them up is 30 minutes.
    aka, if driver drove > 30 blocks
"""

class Driver(object):
    uid = None
    coords_pickup = None
    coords_dropoff = None
    coords_curr = None
    hail_id = None
    start_time = 0
    trip_duration = 0


    def __init__(self, uid=None, pickup=None, dropoff=None, curr=None, hail=None, seed=True):
        self.uid = uid
        self.coords_pickup = pickup
        self.coords_dropoff = dropoff
        self.coords_curr = curr
        self.hail_id = hail
        self.start_time = 0
        self.trip_duration = 0

        if seed:
            self._rand_unseeded()


    def _rand_unseeded(self):
        """
        Initialize the Hail with pseudorandom values for any unset fields.
        """
        if not self.coords_pickup:
            self.coords_pickup = (random.randint(*RANGE_GRID), random.randint(*RANGE_GRID))
        while not self.coords_dropoff:
            drop = (random.randint(*RANGE_GRID), random.randint(*RANGE_GRID))
            if drop != self.coords_pickup:
                self.coords_dropoff = drop
        if not self.coords_curr:
            self.coords_curr = (random.randint(*RANGE_GRID), random.randint(*RANGE_GRID))
    
    def duration(self, x1, x0, y1, y0):
        return math.fabs(x1 - x0) + math.fabs(y1 - y0)

    def attempt_assign(self, hailer, time):
        #ignore is to literally do nothing. no changes
        #returns True/False if assigned successfully
        """
        The minimum distance a driver is willing to take a rider is 5 blocks;
        hails that do not meet this distance are (politely) ignored.
        The maximum distance a driver is willing to take a rider is 100 blocks;
        hails that exceed this distance are also ignored.
        """
        x1 = hailer.coords_dropoff[0]
        y1 = hailer.coords_dropoff[1]
        x0 = hailer.coords_pickup[0]
        y0 = hailer.coords_pickup[1]
        trip_dist = self.duration(x1, x0, y1, y0)

        #ignore cases
        if trip_dist > 100 or trip_dist < 5:
            return False
        self.hail_id = hailer.uid
        self.coords_pickup = hailer.coords_pickup
        self.coords_dropoff = hailer.coords_dropoff
        self.start_time = time
        self.trip_duration = trip_dist
        #print("driver's start time is : %d" % (self.start_time) )
        return True

    def drop_off(self):
        self.coords_curr = self.coords_dropoff
        self.coords_pickup = (0,0)
        self.coords_dropoff = (0,0)
        #remove the rider
        self.hail_id = None
        #print("dropped off")

    def cancel(self):
        self.coords_pickup = (0,0)
        self.coords_dropoff = (0,0)
        self.hail_id = None
    
        #print("cancelled")

    def __str__(self):
        return '%(uid)s|%(pickx)s,%(picky)s|%(dropx)s,%(dropy)s|%(currx)s,%(curry)s|%(st)s|%(dr)s' % dict(
            uid=self.uid,
            pickx=self.coords_pickup[0],
            picky=self.coords_pickup[1],
            dropx=self.coords_dropoff[0],
            dropy=self.coords_dropoff[1],
            currx=self.coords_curr[0],
            curry=self.coords_curr[1],
            st=self.start_time,
            dr=self.trip_duration,
        )
        #return '{c}|{u}|{d}|{t}'.format(c=self.__class__.__name__, u=self.uid, d=self.distance, t=self.timestamp)
