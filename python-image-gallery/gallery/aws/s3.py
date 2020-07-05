import logging
import boto3
from botocore.exceptions import ClientError


def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def get_object(bucket_name, key):
    try:
            s3_client = boto3.client('s3')
            result =  s3_client.get_object(Bucket=bucket_name, Key=key)
    except ClientError as e:
        logging.error(e)
        return None
    return result


def put_object(bucket_name, key, value):
    # Create bucket
    try:
            s3_client = boto3.client('s3')
            s3_client.put_object(Bucket=bucket_name, Key=key, Body=value, ACL='public-read')
    
    except ClientError as e:
        logging.error(e)
        return False
    return True

def list_files(bucket_name, prefix):
    try:
            s3_client = boto3.client('s3')
            contents = [] 
            for item in s3_client.list_objects(Bucket=bucket_name,Prefix=prefix)['Contents']:
                contents.append(item['Key'])
    except ClientError as e:
        logging.error(e)
        return None
    return contents

def upload_file_to_s3(file, bucket_name, acl="public-read"):
    try:
        s3_client = boto3.client('s3') 
        s3_client.upload_fileobj(file, bucket_name, file.filename, ExtraArgs={ "ACL": acl, "ContentType": file.content_type })

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    return True

def main():
# create_bucket('adkins-bucket-2', 'us-west-1')
# put_object('adkins-bucket-2', 'banana', 'yellow') 
  #  print(get_object('adkins-bucket-2','banana')['Body'].read())
  print(list_files('adkins-bucket-2', 'jim')[0])

if __name__ == "__main__":
    main()
