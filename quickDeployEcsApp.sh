#! /bin/bash -eu
cd aws-cfns/

# VPC
echo
echo VPC
aws cloudformation deploy \
    --template-file vpc.yaml \
    --stack-name tsp-vpc

# SecurityGroup
echo
echo SecurityGroup
aws cloudformation deploy \
    --template-file securitygroup.yaml \
    --stack-name tsp-securitygroup

# CodeCommit
echo
echo CodeCommit
aws cloudformation deploy \
    --template-file codecommit.yaml \
    --stack-name tsp-codecommit

# git push to CodeCommit
cd ../
git clone https://git-codecommit.ap-northeast-1.amazonaws.com/v1/repos/tsp-codecommit-py-app
cd appContainer/
cp -r * ../tsp-codecommit-py-app/
cd ../tsp-codecommit-py-app/
git add .
git commit -m "init commit"
git push
cd ../aws-cfns/

# ECR
echo
echo ECR
aws cloudformation deploy \
    --template-file ecr.yaml \
    --stack-name tsp-ecr

aws ecr put-image-scanning-configuration --repository-name tsp-ecr-py-app --image-scanning-configuration scanOnPush=true

# Push App to ECR
cd ../tsp-codecommit-py-app/
aws --version
$(aws ecr get-login --region ap-northeast-1 --no-include-email)
ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
IMAGE_URI=${ACCOUNT_ID}.dkr.ecr.ap-northeast-1.amazonaws.com/tsp-ecr-py-app
docker build -t ${IMAGE_URI}:latest .
docker push ${IMAGE_URI}:latest
cd ../aws-cfns/

# ECS-Cluster
echo
echo ECS Cluster
aws cloudformation deploy \
    --template-file ecs-cluster.yaml \
    --stack-name tsp-ecs-cluster

# App-ALB-Fargate
echo
echo App ALB Fargate
aws cloudformation deploy \
    --template-file app-alb-fargate.yaml \
    --stack-name tsp-app-alb-fargate \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides \
    ImageUri=${IMAGE_URI}

# CodePipeLine
echo
echo CodePipeLine
aws cloudformation deploy \
    --template-file app-codepipeline.yaml \
    --stack-name tsp-app-codepipeline \
    --capabilities CAPABILITY_IAM

echo
echo "[Success] All templates are deployed."
echo
app_url=$(aws cloudformation describe-stacks --stack-name tsp-app-alb-fargate | jq '.Stacks'[0]'.Outputs'[4]'.OutputValue')
echo App URL: ${app_url}
