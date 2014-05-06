from datetime import datetime
import gzip, re
import sys, os
from collections import defaultdict
from glob import glob
sys.path.append('/home/bennet/python/abbot')
from functions import *

# Set these as '' to be a wildcard, otherwise set a value for one
# or more of the period
year = '2013'
month = '10'
# day = '[0-9]*'
day = '15'
# hostnames = 'flux[12]'
hostnames = 'flux[12]'
dataDir = '/usr/flux/logs'

# Use for debugging...
# logfiles = [ '/usr/flux/logs' + '/module_log-flux1-2020-10-05.gz',
#              '/usr/flux/logs' + '/module_log-flux2-2020-10-05.gz']

# Create the filename glob string
logfiles = dataDir + '-'.join(['/module_log', hostnames, year, month, day]) + '.gz'

def readZippedLog(zippedLog):
    '''Reads the zip file supplied as an argument and returns just the date,
       user, module, and version'''
    year = getLogYear(zippedLog)
    log = gzip.open(zippedLog, 'r')
    entries = []
    for line in log:
        # Some lines have the trailing 'flux' field; use the slice to insure
        # only seven entries are used
        [ month, day, time, host, user, module, version ] = line.split()[0:7]
        # Strip the trailing colon from the user name
        user = user.rstrip(':')
        # Construct a datetime object from the components
        date = datetime.strptime(month + ' ' + day + ' ' + str(year) + ' ' + time,
                                 '%b %d %Y %H:%M:%S')
        entries.append( [date, user, module, version] )
    log.close()
    # print "Read %d lines from log" % N
    return entries

logEntries = []
for zippedLog in glob(logfiles):
    # print "Year for %s is %d" % (zippedLog, year)
    logEntries += readZippedLog(zippedLog)

print "Printing first five log entries"
print logEntries[0:5]
