#!/usr/bin/env python

import sys, os
from datetime import datetime
import gzip, re
from collections import defaultdict
from glob import glob

# import the functions for the module reporter
sys.path.append('/home/bennet/python/abbot')
from functions import *

# Initialize entries as a list
entries = []
report = defaultdict(dict)

# Set the report type:  daily, monthly, yearly
period = "monthly"

# Set these as '' to be a wildcard, otherwise set a value for one
# or more of the period
year = '2013'
month = '10'
day = ''
hostnames = 'flux[12]'

# Set the log file directory here
dataDir = '/usr/flux/logs'

# We used to change to the directory, but that's bad, as we want to
# be able to run from someplace we can write without being root.
if os.path.isdir(dataDir):
    pass
else:
    print "No data directory"
    sys.exit(9)

# Assign glob wildcards if these are empty
if year == '':
    year = '[0-9]*'

if month == '':
    month = '[0-9]*'

if day == '':
    day = '[0-9]*'

# Create the filename glob string
logfiles = dataDir + '-'.join(['/module_log', hostnames, year, month, day]) + '.gz'

# Use a constant for debugging...
# logfiles = logpath + '/module_log-flux2-2013-10-05.gz'

for zippedLog in glob(logfiles):
    # Extract the year from the filename
    year = getLogYear(zippedLog)
    log = gzip.open(zippedLog, 'r')
    logEntries = readZippedLog(zippedLog)

        # Change the definition for the date key based on report period
        # defined at the top.  Eventually, this might be a command line
        # option.        
        if period == "daily":
            str_date = date.strftime('%Y-%m-%d')
        elif period == "monthly":
            str_date = date.strftime('%Y-%m')
        elif period == "yearly":
            str_date = date.strftime('%Y')

        if str_date not in report:
            # No date yet?  Initialize it with the current module
            report[str_date] = { module : 1 }
        else:
            # Date is there, so look for the module key: create and set to 1
            # or add 1 to it for this occurrence.
            if module not in report[str_date]:
                report[str_date][module] = 1
            else:
                report[str_date][module] += 1
        # End processing the line from the log file
    f.close()
    
# Print the summary report based on the time period.
for d in report:
    for m in report[d]:
        print "%s module %-35s usage was %d" % (d, m, report[d][m])
