
import argparse
import sys
import csv
import string
import datetime
import calendar
import os
#from apiclient.errors import HttpError
from apiclient import sample_tools
from oauth2client.client import AccessTokenRefreshError
from datetime import date
from dateutil.relativedelta import relativedelta

t=date.today()
print calendar.mdays[datetime.date.today().month]
#change to run path for google client
os.chdir("/Library/Python/2.7/site-packages")
#os.environ['PYTHONPATH']='/Library/Python/2.7/site-packages'

class SampledDataError(Exception): pass

today=datetime.date.today()
#previousdate=today + datetime.timedelta(days=-today.weekday()-2)
lm=today - relativedelta(months=3)
firstdaymonth=date(lm.year,lm.month,1)
lastdaymonth=date(lm.year, lm.month, calendar.mdays[lm.month])
last_month_start=firstdaymonth.strftime('%Y-%m-%d')
last_month_end=lastdaymonth.strftime('%Y-%m-%d')
print lastdaymonth
print firstdaymonth
FDM=firstdaymonth.strftime('%Y-%m-%d')
LDM= lastdaymonth.strftime('%Y-%m-%d')





def main(argv):
  # Authenticate and construct service.
  #pass config file to this py,  argv[0] is the script itself,  argv[1] will be the file name(full path and file name)
  sTemp=argv[0]
  argv2 = [sTemp]
  service, flags = sample_tools.init(
      argv2, 'analytics', 'v3', __doc__, __file__,
      scope='https://www.googleapis.com/auth/analytics.readonly')

  # Try to make a request to the API. Print the results or handle errors.

  with open(argv[1]) as f:
      lines = f.readline()  # read first line
      lines = "" #skip the first line
      lines = f.read().splitlines()
      for l in lines:
          config = l.split("|")
          #  config[0] is  Platform, config[1]Profile_id,config[2]dimensions config[3]metrics config[4]start_date  config[5] end_date config[6]:file name


          try:
            profile_id = config[1]
            print 'Starting downloading...' + config[0]
            if not profile_id:
              print 'No valid profile for user.'
            else:
                start_dt=eval(config[4])
                end_dt=eval(config[5])

                limit = ga_query(service, profile_id, config[2],config[3],0,
                                         start_dt, end_dt).get('totalResults')
                for pag_index in xrange(0, limit, 1000000):
                  results = ga_query(service, profile_id,config[2],config[3], pag_index,
                                     start_dt, end_dt)
                if results.get('containsSampledData'):
                    #raise SampledDataError # if you dont mind sampled data, put a #in from of the raise sampleldata
                    print "*******  Note"
                    print "sampled"
                    print "************************************************"

                print_results(results, pag_index, start_dt, end_dt,config[6],config[0])

          except TypeError, error:
            # Handle errors in constructing a query.
            print ('Error constructing query : %s' % error)

#          except HttpError, error:
            # Handle API errors.
#           print ('Arg, there was an API error : %s : %s' %
#                  (error.resp.status, error._get_reason()))

          except AccessTokenRefreshError:
            # Handle Auth errors.
            print ('The credentials have been revoked or expired, please re-run '
                   'the application to re-authorize')

          except SampledDataError:
            # force an error if ever a query returns data that is sampled!
            print ('Error: Query contains sampled data!')


def ga_query(service, profile_id, dims, mtrs, pag_index, start_date, end_date):

  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=start_date,
      end_date=end_date,
      metrics=mtrs,
      dimensions= dims,
      #sort='-ga:yearWeek',
      #filters='ga:dimension50==notification',
      samplingLevel='HIGHER_PRECISION',
      #start_index=str(pag_index+1),
      max_results=str(pag_index+100000)).execute()

def print_results(results, pag_index, start_date, end_date,file_name,plat_form):
  """Prints out the results.

  This prints out the profile name, the column headers, and all the rows of
  data.

  Args:
    results: The response returned from the Core Reporting API.
  """
  platform= plat_form
  print platform
  filename = file_name+start_date+'_'+ end_date+'.csv'
  f = open( filename, 'wt')
  writer = csv.writer(f, lineterminator='\n')
  write_headers = True
  first_headers = []

  # New write header
  if int(pag_index) == 0:
      print 'Profile Name: %s' % results.get('profileInfo').get('profileName')
      columnHeaders = results.get('columnHeaders')
      cleanHeaders = [str(h['name']) for h in columnHeaders]
      #writer.writerow(cleanHeaders)
      print 'Now pulling data from %s to %s.' %(start_date, end_date)



  # Print data table.
  if results.get('rows', []):
    for row in results.get('rows'):
      for i in range(len(row)):
        old, new = row[i], str()
        for s in old:
          new += s if s in string.printable else ''
        row[i] = new
      row = [platform]+row
      print row
      writer.writerow(row)

  else:
    print 'No Rows Found'

  limit = results.get('totalResults')
  print pag_index, 'of about', int(round(limit, -4)), 'rows.'
  return None


  f.close()

if __name__ == '__main__': main(sys.argv)

print "All profiles done."