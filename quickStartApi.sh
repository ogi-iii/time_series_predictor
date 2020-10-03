#! /bin/bash
cd api/

# TSPUploadLambdaApi
echo
echo "[1/3] Deploying tsp-upload-api..."
echo
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
echo
echo "[2/3] Deploying tsp-hist-api..."
echo
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

# Edit Dockerfile
echo
echo "[3/3] Write endpoints in Dockerfile..."
echo
cd ../../
sed -e '$d' Dockerfile > temp.txt
rm Dockerfile
mv temp.txt Dockerfile
sudo yum -y install jq
uploadapi=$(aws cloudformation describe-stacks --stack-name tsp-upload-api | jq '.Stacks'[0]'.Outputs'[0]'.OutputValue')
echo tsp-upload-api ${uploadapi}
echo
histapi=$(aws cloudformation describe-stacks --stack-name tsp-hist-api | jq '.Stacks'[0]'.Outputs'[0]'.OutputValue')
echo tsp-hist-api ${histapi}
echo
echo CMD [${uploadapi}, ${histapi}] >> Dockerfile
echo "[Success] All shell tasks are completed."
