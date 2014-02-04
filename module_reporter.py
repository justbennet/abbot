#!/usr/bin/env python

from datetime import datetime
import gzip, re
import sys, os
from collections import defaultdict
from glob import glob

# Initialize entries as a list
entries = []
report = defaultdict(dict)

# Set the location of the folder for the processed data
# report_dir = '/home/bennet/python/abbot'
report_dir = '/Users/bennet/python/abbot'

# Set the report type:  daily, monthly, yearly
period = "monthly"

# Set these as '' to be a wildcard, otherwise set a value for one
# or more
year = '2013'
month = '10'
day = ''
hostnames = 'flux[12]'

# Set raw data and summary log file names based on report type and period
if period == 'monthly':
    raw_file = '/Users/bennet/abbot/' + '-'.join((year, month))

print "The raw data file will be:  " + raw_file

# Set the log file directory here
data_dir = '/Users/bennet/python/abbot/logs'
# data_dir = '/usr/flux/logs'

# We used to change to the directory, but that's bad, as we want to
# be able to run from someplace we can write without being root.
if os.path.isdir(data_dir):
    pass
else:
    print "No data directory"

# Assign glob wildcards if these are empty
if year == '':
    year = '[0-9]*'

if month == '':
    month = '[0-9]*'

if day == '':
    day = '[0-9]*'

# Create the filename glob string
logfiles = data_dir + '-'.join(['/module_log', hostnames, year, month, day]) + '.gz'

# Can use a constant for debugging...
# logfiles = logpath + '/module_log-flux2-2013-10-05.gz'

for zipped_log in glob(logfiles):
    # Extract the year from the filename
    year = str(re.search('/module_log-flux[12]-(?P<year>[\d]{4})-\d{2}-\d{2}.gz',
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

use_list = []

# Print the summary report based on the time period.
for d in report:
    for m in report[d]:
        # print "%s module %-35s usage was %d" % (d, m, report[d][m])
        # print "%-35s %d" % (m, report[d][m])
        use_list.append((m, report[d][m]))

use_list.sort()
for e in use_list:
    print "%-35s %d" % e