import boto3, botocore
from flask import render_template
from helpers import *
from pymongo import MongoClient
from config import S3_LOCATION

def upload_file_to_s3(file, bucket_name, acl="public-read"):

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e + render_template('uploadfail.html')

    photo = {"local":"{}{}".format(S3_LOCATION, file.filename),
            "valid" : False}

    return mongo_insert(photo)
   
    
def mongo_insert(photo):
    try:
        connection = mongo_connect()
        connection.insert_one(photo)
    except Exception as e:
        return e

    return render_template('uploadsuccess.html')

def mongo_connect():
    client = MongoClient('mongodb://galleryuser:123@gallerycluster-shard-00-00-wrtmw.mongodb.net:27017,gallerycluster-shard-00-01-wrtmw.mongodb.net:27017,gallerycluster-shard-00-02-wrtmw.mongodb.net:27017/test?ssl=true&replicaSet=GalleryCluster-shard-0&authSource=admin&retryWrites=true')
    db = client['gallerydb']
    collection = db['gallery']
    return collection

def mongo_list_unvalid():
    connection = mongo_connect()
    pending_approval = connection.find({"valid" : False})
    return pending_approval

def mongo_list_approved():
    connection = mongo_connect()
    approved = connection.find({"valid" : True})
    return approved

def mongo_validate(o_id):
    connection = mongo_connect()
    photo.update
    pass