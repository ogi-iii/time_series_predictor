# Quick Start

'''
aws s3 mb s3://tsp-api-ogi

cd tsp-upload/

aws cloudformation package \
     --template-file template.yaml \
     --s3-bucket tsp-api-ogi \
     --output-template-file packaged-template.yaml

aws cloudformation deploy \
     --template-file ./packaged-template.yaml \
     --stack-name tsp-upload-api \
     --capabilities CAPABILITY_IAM
'''