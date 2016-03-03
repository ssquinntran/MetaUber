# Hailstorm Data Generator

This is a rudimentary means of streaming data to a file, which can then
be read by an application to mimic a variable stream of data. With default
parameters (no arguments passed), it will vary the volume of data based on
a simple algebraic representation of "transportation activity swells" during
the day, depending on the current time that the script is being run at.

## Prerequisites

* python2.7 (python2.6 _may_ work but has not been tested) and pip

## Getting Started

_n.b.: it's suggested to run this in a **virtualenv** environment_
1. `cd /path/to/hailstorm`
2. `virtualenv . && . bin/activate`
3. `pip install -r requirements.txt`
4. `fab`

## Notes

* `fab -- -h` will show you the full list of available options
* `fab -- -d` will write lines to STDOUT as well as `outfile` (see `fab -- -h`)

©2015 UATC. Do not reuse or redistribute.
