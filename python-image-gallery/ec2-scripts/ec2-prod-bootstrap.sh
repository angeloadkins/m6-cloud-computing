#!/usr/bin/bash

export IMAGE_GALLERY_BOOTSTRAP_VERSION="1.1"

aws s3 cp s3://adkins-bucket/ec2-prod-latest.sh ./
/usr/bin/bash ec2-prod-latest.sh
