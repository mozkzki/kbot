#!/bin/bash -eu

# cdk deploy 時に必要
export CDK_AWS_ACCOUNT=dummy
export CDK_AWS_REGION=ap-northeast-1
export PHASE=dev

# lambda 実行時に必要
export LINE_CHANNEL_ACCESS_TOKEN=dummy
export LINE_CHANNEL_SECRET=dummy
export LINE_SEND_ID_1=dummy
export LINE_SEND_GROUP_ID_1=dummy
export LIBRARY_CHECK_RENTAL_FUNCTION_ARN=dummy
export LIBRARY_CHECK_EXPIRE_FUNCTION_ARN=dummy
export LIBRARY_CHECK_RESERVE_FUNCTION_ARN=dummy
export LIBRARY_CHECK_PREPARE_FUNCTION_ARN=dummy
