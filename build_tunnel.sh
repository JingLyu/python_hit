#!/usr/bin/python

from sshtunnel import SSHTunnelForwarder
import sys

import os        



    

#http://stackoverflow.com/questions/22046708/
#https://github.com/pahaz/sshtunnel

#at least wrap in a try except block
if 1==1: 
    server = SSHTunnelForwarder(
        ('10.32.220.20', 22),
        ssh_username="user",
        ssh_password="password",
        remote_bind_address=('hostname', 5432),# this needs to be the port on the remote server,
        local_bind_address=('127.0.0.1', 1234) #this can be whatever you want
    )
    server.start()
    print ("tunnel for moderator started through shell server")
       
