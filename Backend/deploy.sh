#!/bin/bash

TEMPLATEFILE=.aws-sam/build/template.yaml
PACKAGEFILE=.aws-sam/build/package.yaml
AWSPROFILE=default
S3=taxidi-code
STACKNAME=taxidi

# need only for local testing and for online editor
sam build

# validate template.yaml
sam validate

sam package \
    --template-file $TEMPLATEFILE\
    --output-template-file $PACKAGEFILE \
    --s3-bucket $S3 \
    --profile $AWSPROFILE

sam deploy \
    --template-file $PACKAGEFILE \
    --stack-name $STACKNAME \
    --capabilities CAPABILITY_NAMED_IAM \
    --profile $AWSPROFILE \
    --parameter-overrides ProjectName=$STACKNAME