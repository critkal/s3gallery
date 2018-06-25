import os

S3_BUCKET		= "critkal-bucket-test"
S3_KEY			= "AKIAJ6QXHN6MPEEHNWVA"
S3_SECRET		= "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"
S3_LOCATION		= 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

SECRET_KEY 		= os.urandom(32)
DEBUG			= True
PORT			= 5000