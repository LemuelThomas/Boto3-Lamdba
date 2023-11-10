# This script lists all S3 buckets in your AWS account

import boto3

s3 = boto3.resource('s3')

# List all S3 Buckets
for bucket in s3.buckets.all():
    print(bucket.name)
