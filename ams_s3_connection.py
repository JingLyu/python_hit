#!/usr/bin/python

## import the module
from boto.s3.connection import S3Connection

## create connection to the service
conn = S3Connection('AKIAIVLIL4SWC3FQARMQ', '0Jne6LwygDnjU3T17bsIe+qscAdIApjd8RMkGXGJ')

## creating a bucket
bucket = conn.get_bucket('de-case-study-qb')

## uploading data


## downloading data
from boto.s3.key import Key
key_obj = Key(bucket)
key_obj.key = 'Part_Costs.xlsx'

contents = key_obj.get_contents_as_string()

## Download data into a file
key_obj.get_contents_to_filename('Part_Costs.xlsx')

## deleting a file
#key_deleted = bucket.delete_key('my_file_1')

## list files/keys in a bucket
#rs_keys = bucket.get_all_keys()

## now, let's look at some miscellaneous operations
## get a list of all the buckets available

## returns ResultSet object
#rs_buckets = conn.get_all_buckets()

#for bucket_obj in rs_buckets:
#    print bucket_obj.name