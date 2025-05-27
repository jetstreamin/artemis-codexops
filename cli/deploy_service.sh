#!/bin/bash
# Deploy a new Artemis CodexOps microservice to AWS using CloudFormation

set -e

if [ "$#" -lt 5 ]; then
  echo "Usage: $0 <service-name> <container-image> <container-port> <database-url> <s3-bucket>"
  exit 1
fi

SERVICE_NAME="$1"
CONTAINER_IMAGE="$2"
CONTAINER_PORT="$3"
DATABASE_URL="$4"
S3_BUCKET="$5"

STACK_NAME="codexops-${SERVICE_NAME}"

aws cloudformation deploy \
  --template-file artemis-codexops/cloudformation-service-module.yaml \
  --stack-name "$STACK_NAME" \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    ServiceName="$SERVICE_NAME" \
    ContainerImage="$CONTAINER_IMAGE" \
    ContainerPort="$CONTAINER_PORT" \
    DatabaseUrl="$DATABASE_URL" \
    S3Bucket="$S3_BUCKET"

echo "Deployed $SERVICE_NAME as stack $STACK_NAME."
