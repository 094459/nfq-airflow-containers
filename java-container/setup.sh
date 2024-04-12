#!/usr/bin/env bash

# Change these values for your own environment
# it should match what values you use in the CDK app
# if you are using this script together to deploy
# the multi-arch demo

AWS_DEFAULT_REGION=ap-southeast-1
AWS_ACCOUNT=704533066374
AWS_ECR_REPO=nfq-airflow-images
COMMIT_HASH="airflw"

# You can alter these values, but the defaults will work for any environment

IMAGE_TAG=${COMMIT_HASH:=latest}
#PROC_TAG=${COMMIT_HASH}-aarch64
PROC_TAG=${COMMIT_HASH}-amd64

DOCKER_CLI_EXPERIMENTAL=enabled
REPOSITORY_URI=$AWS_ACCOUNT.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$AWS_ECR_REPO

# Login to ECR
# Old deprecated
# $(aws ecr get-login --region $AWS_DEFAULT_REGION --no-include-email)
aws ecr get-login-password --region $AWS_DEFAULT_REGION | finch login --username AWS --password-stdin $AWS_ACCOUNT.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com

# create AWS ECR Repo

if (aws ecr describe-repositories --repository-names $AWS_ECR_REPO ) then
	echo "Skipping the create repo as already exists"
else
	echo "Creating repos as it does not exists"
	aws ecr create-repository --region $AWS_DEFAULT_REGION --repository-name $AWS_ECR_REPO
fi

# Build initial image and upload to ECR Repo

#finch build -t $REPOSITORY_URI:latest .
finch build --platform=linux/amd64 -t $REPOSITORY_URI:$PROC_TAG .
finch tag $REPOSITORY_URI:$PROC_TAG $REPOSITORY_URI:$PROC_TAG
finch push $REPOSITORY_URI:$PROC_TAG
