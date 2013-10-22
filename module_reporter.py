#!/usr/bin/env python

from datetime import datetime
import glob, gzip, re
import sys, os
from collections import defaultdict

# Set the report type:  daily, monthly, yearly
period = "monthly"

#  Set the log file directory here
# data_dir = '/home/bennet/python/logmunger/data'
data_dir = '/usr/flux/logs'
if os.path.isdir(data_dir):
    os.chdir(data_dir)
else:
    print "No data directory"

# Get the list of filenames from the log directory
#   At some point this should be limitable to, say one month

logfiles = glob.glob('./*.gz')
# for debugging, use just one file
# logfiles = [ './module_log-flux2-2013-10-05.gz', './module_log-flux1-2013-10-05.gz' ]

# Initialize entries as a list
entries = []
report = defaultdict(dict)

for zipped_log in logfiles:
    # Extract the year from the filename
    year = str(re.match('./module_log-flux[12]-(?P<year>[\d]{4})-\d{2}-\d{2}.gz',
                     zipped_log).group('year'))
    # print "Working on %s" % zipped_log
    # Open the log file
    f = gzip.open(zipped_log, 'r')
    N = 0
    for line in f:
        # if N == 0: print line
        N += 1
        # Some lines have the trailing 'flux' field; use the slice to insure
        # only seven entries are used
        [ month, day, time, host, user, module, version ] = line.split()[0:7]
        # Strip the trailing colon
        user = user.rstrip(':')
        # Construct a datetime object from the components
        date = datetime.strptime(month + ' ' + day + ' ' + year + ' ' + time,
                                 '%b %d %Y %H:%M:%S')
        module = module + '/' + version
        # Add user and module to the entry
        entry = [ date, ]
        entry = entry + [ user, ]
        entry = entry + [ module, ]
        entries.append(entry)

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
