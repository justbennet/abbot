import re, time, gzip

def getLogYear(logFileName):
    '''Extract the year from the filename'''
    year = str(re.search('/module_log-flux[12]-(?P<year>[\d]{4})-\d{2}-\d{2}.gz',
                     logFileName).group('year'))
    return int(year)

def readZippedLog(zippedLog):
    '''Reads the zip file supplied as an argument and returns just the date,
       user, module, and version'''
    year = getLogYear(zippedLog)
    log = gzip.open(zippedLog, 'r')
    for line in log:
        # Some lines have the trailing 'flux' field; use the slice to insure
        # only seven entries are used
        [ month, day, time, host, user, module, version ] = line.split()[0:7]
        # Strip the trailing colon from the user name
        user = user.rstrip(':')
        # Construct a datetime object from the components
        date = datetime.strptime(month + ' ' + day + ' ' + year + ' ' + time,
                                 '%b %d %Y %H:%M:%S')
        entries.append( [date, user, module, version] )
    f.close()
    return entries

def reportMonth(month, year):
    if year == 0:
        #  Set year to this year
        year = time.localtime()[0]
        print "Running report for %d, %d" % (int(month), int(year))
    else:
        year = int(year)
        print "Running report for %d, %d" % (int(month), int(year))

def reportYear(year):
    print "Running report for year %d" % int(year)

def reportRange(monthRange, yearRange):
    print "Running report from %d/%d to %d/%d" % \
           (int(monthRange[0]), int(yearRange[0]), \
            int(monthRange[1]), int(yearRange[1]))
