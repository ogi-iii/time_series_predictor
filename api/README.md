# Quick Start

'''
cd api/

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
'''