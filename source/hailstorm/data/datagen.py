# vim: set fileencoding=utf-8 :

from __future__ import absolute_import, print_function
import math
import os
import signal
import sys
import time
from datetime import date, datetime, timedelta
# ---
from hailstorm.data.hail import Hail


local_epoch = datetime(*date.today().timetuple()[:-2])
interrupt = False

def gen(timestamp=None, generator_epoch=None):
    """
    Emit a series of Hail records with a particular frequency distribution.

    :param timestamp: injectable timestamp for current time
    :param generator_epoch: injectable reference moment for starting the series
    :return: a Hail request at a suitably random moment
    """
    now = timestamp if timestamp is not None and isinstance(ts, datetime) else datetime.now()
    generator_epoch = generator_epoch if generator_epoch is not None else local_epoch
    canonical_epoch = datetime(1969, 12, 31, 19)  # EST simulation

    while not interrupt:
        delta = (now - generator_epoch).total_seconds() / 3600
        coeff = _get_freq_coeff(delta)
        snooze = 1.0 / coeff

        yield Hail(timestamp=(now - canonical_epoch).total_seconds())

        now = now + timedelta(seconds=snooze)

    sys.exit(0)


def _get_freq_coeff(x):
    # See: https://www.desmos.com/calculator/kgmnznvqhx
    #coeff = (2.25 * math.sin(((math.pi / 6) * x) + 3.25)) + 2.75
    coeff = (2.25 * (math.cos(((math.pi / 4) * x) + 1.5) * math.cos(((math.pi / 2.5) * x) + 4))) + 2.75
    return coeff


def _handle_sigint(*args):
    global interrupt
    interrupt = True


signal.signal(signal.SIGINT, _handle_sigint)
__all__ = ['gen']
