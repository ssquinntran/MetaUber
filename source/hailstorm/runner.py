"""The hailstorm runner.

Usage:
    runner.py [options]

Examples:
    runner.py --time=13:22
    runner.py --outfile=/var/log/mydata.log
    runner.py -t 13:22 -o /var/log/mydata.log
    runner.py (-h | --help)

Options:
    -d --debug              Enable debug output (stdout)
    -o --outfile=<p>        Specify an outfile [default: hailstorm.out]
    -t --time=<t>           Override the current time of day.
                            Note: please use HH:MM formatting.
    -h --help               Show this screen
"""


from __future__ import absolute_import, print_function
import os
import re
import sys
from datetime import datetime
# ---
from docopt import docopt



try:
    from hailstorm.data import datagen
except ImportError:
    __root__ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.append(__root__)
    from hailstorm.data import datagen


def stream_to_file(outfile, when, debug=False):
    """
    Run a hail generator and stream the results into a file for later consumption.

    :param outfile: output file name
    :param when: hail generator starting timestamp
    :param debug: whether to log debugging output
    :return:
    """
    with open(outfile, 'a+') as of:
        for hail in datagen.gen(timestamp=when):
            if debug:
                print(hail)
            print(hail, file=of)

def run():
    """
    Run a simulation.

    :return:
    """
    idx = (sys.argv.index('--') + 1) if '--' in sys.argv else 1
    arguments = docopt(__doc__, argv=sys.argv[idx:])
    debug = arguments.get('--debug')
    outfile = arguments.get('--outfile')
    when = arguments.get('--time')

    for k, v in arguments.items():
        print('{k} = {v}'.format(k=k, v=v))

    if when and not isinstance(when, datetime) and re.match(r'\d{2}:\d{2}', when):
        try:
            when = datetime.strptime('{ymd} {t}'.format(ymd=datetime.now().strftime('%Y-%m-%d'), t=when), '%Y-%m-%d %H:%M')
        except ValueError as e:
            raise(e)

    # Currently, the simulation merely streams simulated Hails into a file.
    stream_to_file(outfile, when, debug=debug)


if __name__ == '__main__':
    run()
