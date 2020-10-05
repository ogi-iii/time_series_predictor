#! /bin/bash -eu
cd api/
ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)

# TSPUploadLambdaApi
echo
echo "Deploy tsp-upload-api"
aws s3 mb s3://tsp-upload-template-${ACCOUNT_ID}
cd tsp-upload/

aws cloudformation package \
    --template-file template.yaml \
    --s3-bucket tsp-upload-template-${ACCOUNT_ID} \
    --output-template-file packaged-template.yaml

aws cloudformation deploy \
    --template-file ./packaged-template.yaml \
    --stack-name tsp-upload-api \
    --capabilities CAPABILITY_IAM

# TSPHistoryLambdaApi
echo
echo "Deploy tsp-hist-api"
aws s3 mb s3://tsp-hist-template-${ACCOUNT_ID}
cd ../tsp-history/

aws cloudformation package \
    --template-file template.yaml \
    --s3-bucket tsp-hist-template-${ACCOUNT_ID} \
    --output-template-file packaged-template.yaml

aws cloudformation deploy \
    --template-file ./packaged-template.yaml \
    --stack-name tsp-hist-api \
    --capabilities CAPABILITY_IAM

# Edit Dockerfile
echo
echo "Write endpoints in Dockerfile"
cd ../../appContainer/
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
cd ../
echo "[Success] All shell tasks are completed."
