#!/bin/bash

# Reference this script from your compose file - make sure that it has access from the volume
echo "-------------------------------------"
echo "Initializing LocalStack resources...."
echo "-------------------------------------"

export AWS_DEFAULT_REGION=ap-southeast-1

# ---- S3 ----
echo "Creating S3 bucket: mypregnancy-bucket"
awslocal s3 mb s3://mypregnancy-bucket

echo "--------------------------------"
echo "LocalStack resources initialized"
echo "--------------------------------"