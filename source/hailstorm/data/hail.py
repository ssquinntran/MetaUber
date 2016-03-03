from __future__ import absolute_import
import random
import time
import uuid


RANGE_GRID = (0,99)


class Hail(object):
    """
    A Hail represents a rider request to travel from and to particular city corners.
    """
    uid = None
    timestamp = None
    coords_pickup = None
    coords_dropoff = None


    def __init__(self, uid=None, timestamp=None, pickup=None, dropoff=None, seed=True):
        self.uid = uid
        self.timestamp = timestamp
        self.coords_pickup = pickup
        self.coords_dropoff = dropoff

        if seed:
            self._rand_unseeded()


    def _rand_unseeded(self):
        """
        Initialize the Hail with pseudorandom values for any unset fields.
        """
        if not self.uid:
            self.uid = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = time.time()
        if not self.coords_pickup:
            self.coords_pickup = (random.randint(*RANGE_GRID), random.randint(*RANGE_GRID))
        while not self.coords_dropoff:
            drop = (random.randint(*RANGE_GRID), random.randint(*RANGE_GRID))
            if drop != self.coords_pickup:
                self.coords_dropoff = drop


    def __str__(self):
        return '%(cls)s|%(uid)s|%(ts).06f|%(pickx)s,%(picky)s|%(dropx)s,%(dropy)s' % dict(
            cls=self.__class__.__name__,
            uid=self.uid,
            ts=self.timestamp,
            pickx=self.coords_pickup[0],
            picky=self.coords_pickup[1],
            dropx=self.coords_dropoff[0],
            dropy=self.coords_dropoff[1],
        )
        #return '{c}|{u}|{d}|{t}'.format(c=self.__class__.__name__, u=self.uid, d=self.distance, t=self.timestamp)
