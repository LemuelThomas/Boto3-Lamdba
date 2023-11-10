# This script uses crud operations on S3 bucket of your choice

#  Import boto3 library
import boto3

#  *Instantiate a boto3 resource for s3 + name the bucket
import botocore.exceptions

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
bucket_name = 'lt-crud-1'

#  Check if bucket already exists
#  *CREATE bucket if it doesn't
all_my_buckets = [bucket.name for bucket in s3.buckets.all()]
if bucket_name not in all_my_buckets:
    print(f"'{bucket_name}' bucket doesn't exist. Creating now...")
    s3.create_bucket(Bucket=bucket_name)
    print(f"'{bucket_name}' bucket has been created.")
else:
    print(f"'{bucket_name}' bucket already exists. No need to create new one.")

#  Upload Files to the new bucket
file1 = 'C:/Users/lemst/OneDrive/Desktop/test/favorite-animal.txt'
file2 = 'C:/Users/lemst/OneDrive/Desktop/test/sky.txt'
objkey1 = 'favorite-animal.txt'
objkey2 = 'sky.txt'

try:
    s3_client.head_object(Bucket=bucket_name, Key=objkey1)
    s3_client.head_object(Bucket=bucket_name, Key=objkey2)
    print(f"Files already exist in the bucket.")
except botocore.exceptions.ClientError as err:
    if err.response['Error']['Code'] == '404':
        s3_client.upload_file(file1, bucket_name, 'favorite-animal.txt')
        s3_client.upload_file(file2, bucket_name, 'sky.txt')
        print(f"Successfully uploaded {file1} AND {file2} to {bucket_name}")
    else:
        print(f"Error: {str(err)}")

#  *READ and print the file from the bucket
obj = s3.Object(bucket_name, objkey2)
body = obj.get()['Body'].read()
print(body)

#  *UPDATE 'file1' in the bucket with new content from 'file2'
# Read the content of 'file2'
with open(file2, 'rb') as file2_content:
    file2_content_data = file2_content.read()
# Update 'file1' in the bucket with the content from 'file2'
s3.Object(bucket_name, objkey1).put(Body=file2_content_data)

# Read and print the updated content of 'file1'
obj = s3.Object(bucket_name, objkey1)
updated_body = obj.get()['Body'].read()
print(updated_body)

try:
    # *DELETE the object in the S3 bucket
    s3_client.delete_object(Bucket=bucket_name, Key=objkey1)
    s3_client.delete_object(Bucket=bucket_name, Key=objkey2)
    print(f"Object '{objkey1}' has been deleted from the bucket.")
    print(f"Object '{objkey2}' has been deleted from the bucket.")
except botocore.exceptions.ClientError as err:
    print(f"Error deleting the object: {str(err)}")

# DELETE the bucket
bucket = s3.Bucket(bucket_name)
bucket.delete()