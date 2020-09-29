#! /bin/bash
cd api/

# TSPUploadLambdaApi
aws s3 mb s3://tsp-upload-template-ogi
cd tsp-upload/

aws cloudformation package \
    --template-file template.yaml \
    --s3-bucket tsp-upload-template-ogi \
    --output-template-file packaged-template.yaml

aws cloudformation deploy \
    --template-file ./packaged-template.yaml \
    --stack-name tsp-upload-api \
    --capabilities CAPABILITY_IAM


# TSPHistoryLambdaApi
aws s3 mb s3://tsp-hist-template-ogi
cd ../tsp-history/

aws cloudformation package \
    --template-file template.yaml \
    --s3-bucket tsp-hist-template-ogi \
    --output-template-file packaged-template.yaml

aws cloudformation deploy \
    --template-file ./packaged-template.yaml \
    --stack-name tsp-hist-api \
    --capabilities CAPABILITY_IAM


# Write endpoints in Dockerfile
cd ../../
sudo yum -y install jq

uploadapi=$(aws cloudformation describe-stacks --stack-name tsp-upload-api | jq '.Stacks'[0]'.Outputs'[0]'.OutputValue')
histapi=$(aws cloudformation describe-stacks --stack-name tsp-hist-api | jq '.Stacks'[0]'.Outputs'[0]'.OutputValue')

echo "[NEXT STEP] add this command to the bottom line in Dockerfile"
echo ""
echo CMD [${uploadapi}, ${histapi}]
echo ""
