#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
from sshtunnel import SSHTunnelForwarder
import sys
import csv
from datetime import datetime,date                       
from dateutil.relativedelta import relativedelta 
import os        

con = None

today = date.today()                                                   
d = today - relativedelta(months=1)                                    
month_begin = date(d.year, d.month, 1)                                 
month_begin_datetime=str(month_begin)+" 00:00:00"                      
month_end = (date(today.year, today.month, 1) - relativedelta(days=1) )
monthe_end_datetime=str(month_end)+" 23:59:59"                         
print (month_begin_datetime,monthe_end_datetime)                       


try:
    

#http://stackoverflow.com/questions/22046708/
#https://github.com/pahaz/sshtunnel

#at least wrap in a try except block
    server = SSHTunnelForwarder(
        ('ip', 22),
        ssh_username="user",
        ssh_password="password",
        remote_bind_address=('sourcehost', 5432),# this needs to be the port on the remote server,
        local_bind_address=('127.0.0.1', 1234) #this can be whatever you want
    )
    print ("111")
    server.start()

    #print(server.local_bind_port)
# work with `SECRET SERVICE` through `server.local_bind_port`.

    #conn = psycopg2.connect(database="dbname",port=server.local_bind_port, user="scott")    
    
    
    
    con = psycopg2.connect("dbname='moderation' port=1234 user='dbuser' host='127.0.0.1' password='dbpassword' ")    
    cur = con.cursor()
    #query = "select version() as ver"
    query = ("SELECT AD_ID as ad_id, reason as reason FROM CS_REVIEW_HISTORY     WHERE DATE BETWEEN '%s' AND '%s' AND REASON IN ('FRAUD','MALICIOUS','PROSTITUTE','SPAM')" % (month_begin_datetime,monthe_end_datetime)  )
    
    print (query)
    outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)
    print (outputquery)
    
    with open('c:\somefile.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        cur.copy_expert(outputquery, f)    
        
    print ("downloaded data successfully")
        
    if con:
        con.close()
    sys.exit()    
except psycopg2.DatabaseError, e:
    print ('error:failed download bad ad')
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()
    sys.exit()    
