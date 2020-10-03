# Time-Series Predictor
![Time-Series Predictor Index Page](./readme_imgs/top_screen.png)

# Functions
Learning & Prediction App for Future Values of Time-Series Data

## CSV Analysis
1. Learn features of data from your csv.  
2. Predict values for the specified period.  
3. Plot the prediction result as a image.  
**It can be downloaded as csv or image!**

### Internal Machine Learning Methods
- SARIMA  
**The others comming soon...**

## Analytics History
1. Catch your previous prediction results from database.  
2. Show them as a table.  
**Each line of the table can be downloaded as csv or plot image!**

# Requirements
## MacOS High Sierra v10.13.6 (local)
- Python 3.7.3
- Docker 19.03.12
- aws-cli 1.18.66
- jupyter-notebook 6.0.0

## AWS Cloud9 (https://aws.amazon.com/cloud9/)
- Python 3.6 (default)
- Docker (default)
- aws-cli (default)

# Usage
You need your own AWS account. (https://aws.amazon.com/)

## Run Local
MacOS High Sierra  

```bash
git clone https://github.com/ogi-iii/time_series_predictor.git
cd time_series_predictor

# Deploy APIs on AWS
quickStartApi.sh
# Run Local Environment
quickRunLocalApp.sh
```

## Deploy on AWS
AWS Cloud9 (https://aws.amazon.com/cloud9/)  

```bash
git clone https://github.com/ogi-iii/time_series_predictor.git
cd time_series_predictor

# Deploy APIs on AWS
quickStartApi.sh
# Create Resources & Deploy on AWS
quickStartEcsApp.sh
```

# Tech Skills
the list of technical skills for creating this app

## AWS  
- Infrastructure as Code  
  - VPC
  - Cloudformation  
  
- Serverless API  
  - Lambda  
  - API Gateway  
  - S3  
  - Dynamo DB  
  
- Container Service  
  - ECS  
  - ECR  
  - Fargate  
  
- CI/CD
  - CodePipeLine  
  - CodeBuild  
  - CodeCommit  

## Others
- Python   
  - flask
  - numpy
  - pandas
  - matplotlib
  - scipy
  - statsmodels  
  - etc.
  
- Machine Learning & Statistics   
  - SARIMA
  
- Docker

- Shell Script

- HTML/CSS

# Reference
## sample-data (AirPassengers.csv)
https://www.analyticsvidhya.com/blog/2016/02/time-series-forecasting-codes-python/
