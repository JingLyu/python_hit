
import argparse
import sys
import csv
import string
import datetime
import calendar
import os

from apiclient.errors import HttpError
from apiclient import sample_tools
from oauth2client.client import AccessTokenRefreshError
from datetime import date
from dateutil.relativedelta import relativedelta

t=date.today()
print calendar.mdays[datetime.date.today().month]


os.chdir("/Library/Python/2.7/site-packages")
class SampledDataError(Exception): pass

today=datetime.date.today()
#previousdate=today + datetime.timedelta(days=-today.weekday()-2)
lm=today - relativedelta(months=1)
firstdaymonth=date(lm.year,lm.month,1)
lastdaymonth=date(lm.year, lm.month, calendar.mdays[lm.month])
print lastdaymonth
print firstdaymonth
FDM=firstdaymonth.strftime('%Y-%m-%d')
LDM= lastdaymonth.strftime('%Y-%m-%d')



def main(argv):
  # Authenticate and construct service.
  service, flags = sample_tools.init(
      argv, 'analytics', 'v3', __doc__, __file__,
      scope='https://www.googleapis.com/auth/analytics.readonly')

  # Try to make a request to the API. Print the results or handle errors.
  try:
    profile_id = profile_ids[profile]
    if not profile_id:
      print 'No valid profile for user.'
    else:
      for start_date, end_date in date_ranges:
        limit = ga_query(service, profile_id, 0,
                                 start_date, end_date).get('totalResults')
        for pag_index in xrange(0, limit, 1000000):
          results = ga_query(service, profile_id, pag_index,
                                     start_date, end_date)
        #if results.get('containsSampledData'):
         #   raise SampledDataError # if you dont mind sampled data, put a #in from of the raise sampleldata
        print_results(results, pag_index, start_date, end_date)

  except TypeError, error:    
    # Handle errors in constructing a query.
    print ('Error constructing query : %s' % error)

  except HttpError, error:
    # Handle API errors.
    print ('Arg, there was an API error : %s : %s' %
           (error.resp.status, error._get_reason()))

  except AccessTokenRefreshError:
    # Handle Auth errors.
    print ('The credentials have been revoked or expired, please re-run '
           'the application to re-authorize')
  
  except SampledDataError:
    # force an error if ever a query returns data that is sampled!
    print ('Error: Query contains sampled data!')


def ga_query(service, profile_id, pag_index, start_date, end_date):

  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=start_date,
      end_date=end_date,
      metrics='ga:sessions, ga:Users',
      dimensions='ga:yearMonth,ga:deviceCategory,ga:channelGrouping, ga:dimension2, ga:dimension1',
      #sort='-ga:yearWeek',
      #filters='ga:dimension50==notification',
      samplingLevel='HIGHER_PRECISION',
      #start_index=str(pag_index+1),
      max_results=str(pag_index+100000)).execute()

def print_results(results, pag_index, start_date, end_date):
  """Prints out the results.

  This prints out the profile name, the column headers, and all the rows of
  data.

  Args:
    results: The response returned from the Core Reporting API.
  """

  # New write header
  if int(pag_index) == 0:
    if (start_date, end_date) == date_ranges[0]:
      print 'Profile Name: %s' % results.get('profileInfo').get('profileName')
      columnHeaders = results.get('columnHeaders')
      cleanHeaders = [str(h['name']) for h in columnHeaders]
      writer.writerow(cleanHeaders)
    print 'Now pulling data from %s to %s.' %(start_date, end_date)



  # Print data table.
  if results.get('rows', []):
    for row in results.get('rows'):
      for i in range(len(row)):
        old, new = row[i], str()
        for s in old:
          new += s if s in string.printable else ''
        row[i] = new
      writer.writerow(row)

  else:
    print 'No Rows Found'

  limit = results.get('totalResults')
  print pag_index, 'of about', int(round(limit, -4)), 'rows.'
  return None

# profile_ids=profile_ids = {'Search':   '72613082',
#                 'Search_to_VIP':  '72613082',
# 			    'Search_to_VIP_to_reply': '72613082',
#                 'zSRP': '72613082',
#                 'VIPs-User': '72613082',
#                 'All_cat_searches': '72613082',
#                 'SeeResults': '72613082',
#                 'SeeResults to NoVIP': '72613082'}

# Uncomment this line & replace with 'profile name': 'id' to query a single profile
# Delete or comment out this line to loop over multiple profiles.

profile_ids = {'Android':  'profile-id'}


date_ranges = [(firstdaymonth.strftime('%Y-%m-%d'),
               lastdaymonth.strftime('%Y-%m-%d'))]
#,
               # ('2012-10-01',
               # '2013-04-30'),
               # ('2013-05-01',
                # '2013-09-30'),
               # ('2013-10-01',
               # '2014-09-30')]

# for profile in sorted(profile_ids):
#   path = 'C:\\Users\\aghellani\\Documents\\Google Analytics Python Data\\' #replace with path to your folder where csv file with data will be written
#   filename = 'google_analytics_data_%s_1.csv' #replace with your filename. Note %s is a placeholder variable and the profile name you specified on row 162 will be written here
#   with open(path + filename %profile.lower(), 'wt') as f:
#     writer = csv.writer(f, lineterminator='\n')
#     if __name__ == '__main__': main(sys.argv)
#   print "Profile done. Next profile..."

#print "All profiles done."

#path = 'C:\\Users\\aghellani\\Documents\\Google Analytics Python Data\\' #replace with path to your folder where csv file with data will be written
path = "/Users/jilv/scripts/"
filename = 'google_analytics_data_PushAndroid.csv' #replace with your filename.
f = open(path + filename, 'wt')
writer = csv.writer(f, lineterminator='\n')
write_headers = True
first_headers = []

for profile in sorted(profile_ids):
  if __name__ == '__main__': main(sys.argv)
  print "Profile done. Next profile..."

f.close()
print "All profiles done."