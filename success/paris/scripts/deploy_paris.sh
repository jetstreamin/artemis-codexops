#!/data/data/com.termux/files/usr/bin/bash

set -e
STACK="ParisAgentStack-v1"
ZIP="paris-lambda.zip"
BUCKET=$(aws s3api list-buckets --query "Buckets[?starts_with(Name, 'paris-agent-deploy')].Name | [0]" --output text)

if [ "$BUCKET" == "None" ] || [ -z "$BUCKET" ]; then
  ID=$(aws sts get-caller-identity --query Account --output text)
  BUCKET="paris-agent-deploy-$ID"
  aws s3 mb s3://$BUCKET
fi

aws s3 cp $ZIP s3://$BUCKET/paris-agent/builds/latest.zip

aws cloudformation deploy \
  --template-file paris-lambda.yaml \
  --stack-name $STACK \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    DeployBucket=$BUCKET \
    DeployKey=paris-agent/builds/latest.zip

echo "✅ Paris deployed. Stack: $STACK | S3: $BUCKET | Key: paris-agent/builds/latest.zip"
