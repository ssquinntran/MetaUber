from __future__ import absolute_import
import os
import sys
# ---
from fabric.api import local, run, task


# since Fabric doesn't support dependencies yet, let's shim it so we can define them
# in the decorator versus explicitly calling them in the function body.
def rtask(requires=None, *args, **kwargs):
    def wrapper(t_fn, *t_args, **t_kwargs):
        if requires:
            table = globals()
            for req in requires:
                req() if callable(req) else table[req]()
        return t_fn(*t_args, **t_kwargs)
    return task(*args, **kwargs)(wrapper)


# get a list of args intended for Fabric (e.g., before any potential --)
def _get_fabric_args():
    idx = sys.argv.index('--') if '--' in sys.argv else -1
    return sys.argv[0:idx]


# ensure the interpreter knows about our source path for lookups, since we're calling it by proxy
def _inject_path():
    p = os.path.abspath(os.path.join(os.path.dirname(__file__), 'source'))
    if p not in sys.path:
        sys.path.append(p)


# call the runner and let it handle additional args/work there (docopt, etc)
@rtask(requires=['_inject_path'], default=True)
def default():
    from hailstorm.runner import run as start
    start()
