#! /bin/bash
cd aws-cfns/

# VPC
echo
echo VPC
echo
aws cloudformation deploy \
    --template-file vpc.yaml \
    --stack-name tsp-vpc

# SecurityGroup
echo
echo SecurityGroup
echo
aws cloudformation deploy \
    --template-file securitygroup.yaml \
    --stack-name tsp-securitygroup

# CodeCommit
echo
echo CodeCommit
echo
aws cloudformation deploy \
    --template-file codecommit.yaml \
    --stack-name tsp-codecommit

# ECR
echo
echo ECR
echo
aws cloudformation deploy \
    --template-file ecr.yaml \
    --stack-name tsp-ecr
aws ecr put-image-scanning-configuration --repository-name tsp-ecr-py-app --image-scanning-configuration scanOnPush=true

# Push App to ECR
cd ../appContainer/
aws --version
$(aws ecr get-login --region ap-northeast-1 --no-include-email)
REPOSITORY_URI=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${IMAGE_NAME}
docker build -t ${REPOSITORY_URI}:latest .
docker push ${REPOSITORY_URI}:latest
cd ../aws-cfns/

# ECS-Cluster
echo
echo ECS Cluster
echo
aws cloudformation deploy \
    --template-file ecs-cluster.yaml \
    --stack-name tsp-ecs-cluster

# App-ALB-Fargate
echo
echo App ALB Fargate
echo
ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
IMAGE_URI=${ACCOUNT_ID}.dkr.ecr.ap-northeast-1.amazonaws.com/tsp-ecr-py-app
aws cloudformation deploy \
    --template-file app-alb-fargate.yaml \
    --stack-name tsp-app-alb-fargate \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides \
    ImageUri=${IMAGE_URI}

# git push to CodeCommit
cd ../appContainer/
git add .
git commit -m "init commit"
git push
cd ../aws-cfns/

# CodePipeLine
echo
echo CodePipeLine
echo
aws cloudformation deploy \
    --template-file app-codepipeline.yaml \
    --stack-name tsp-app-codepipeline

echo
echo "[Success] All templates are deployed."
echo
