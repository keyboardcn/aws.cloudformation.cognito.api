# AWS API Gateway with Cognito Authentication and Lambda Integration

## 📌 Overview

This project demonstrates an AWS-based REST API with secure Cognito authentication 
and two Lambda functions integrating public APIs (OpenWeather and CoinGecko).

## 🔧 Architecture

- **Amazon Cognito** – Handles user authentication.
- **API Gateway** – Exposes RESTful endpoints secured by Cognito.
- **Lambda Functions** – Call:
  - OpenWeatherMap API (Node.js)
  - CoinGecko API (Python)
- **CloudFormation** – Manages infrastructure-as-code.

## 📁 Repository Structure

/aws-api-gateway-assessment
├── README.md
├── cloudformation
│ └── main.yaml
├── lambdas
│ ├── lambda1/index.mjs
│ ├── lambda2/lambda_function.py
└── assets/



## 🚀 Deployment Instructions

### Prerequisites
- AWS CLI and access credentials
- S3 bucket (name: `aws-api-gateway-assessment`) to upload Lambda code


### Steps

1. **Zip and Upload Lambda Functions**
   - install dependencies for node.js
   ```bash
   cd /lambdas/lambda1
   npm install node-fetch
   ```
   - package dependencies into zip files.
   Please refer [Build Node.js .zip file](https://docs.aws.amazon.com/lambda/latest/dg/nodejs-package.html#nodejs-package-create-dependencies), and [Build Python .zip file](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-create-dependencies) for creating zip files
   - upload zip files with aws console, or aws cli
   ```bash
   aws s3 cp lambda1.zip s3://aws-api-gateway-assessment/lambda1.zip 
   aws s3 cp lambda2.zip s3://aws-api-gateway-assessment/lambda2.zip
   ```

2. **Deploy CloudFormation**
    ```bash
    aws cloudformation deploy \
        --template-file cloudformation/main.yaml \
        --stack-name api-cognito-demo \
        --capabilities CAPABILITY_NAMED_IAM \
        --parameter-overrides \
        Lambda1S3Key=lambda1.zip \
        Lambda2S3Key=lambda2.zip
    ```
3. **Set up environment varialbles for nodejs Lambda function**
   OPENWEATHER_API_KEY=<your_api_key>

4. **Note Outputs**
- API URL: your_api_url
- UserPool ID
- Cognito demain: your_domain_url
- App Client ID/secrets: your_app_client_id, your_app_client_secret

### Cognito Setup
**Sign Up a User**
- Go to Cognito > User Pools > `ApiGatewayUserPool`
- Create a test user (with test_username and temporary_password)


###  Testing with postman
1. **Authenticate and Get Token**
- Postman <your_collection>/<your_request> pane, 
- go to tab "Authorization", choose Auth Type OAuth 2.0
- locate "Configure New Token", fill the form as following:
    ```code
    Callback URL: http://localhost:8080/
    Auth URL: <your_domain_url>/oauth2/authorize
    Access Token URL: <your_domain_url>/oauth2/token
    Client ID: <your_app_client_id>
    Client Secret: <your_app_client_secret>
    ```
 - after log in with <test_username> and <temporary_password>, click "Get New Access Token"
 - note the ID token


2. **Test API Endpoints**
- <your_collection>/<your_request> pane, set headers key value pair: {"Authorization": <your_id_token>}
- GET <your_api_url>/weather to test weather endpoint, example output:
  ```json
    {
        "city": "Toronto",
        "temperature": 13.84,
        "weather": "overcast clouds"
    }
  ```
- POST <your_api_url>/crypto to test crypto market endpoint, example output:
  ```json
    {
        "coin": "bitcoin",
        "currency": "usd",
        "price": 102371
    }
  ```
### External Service Used
[OpenWeatherMap API](https://openweathermap.org/api)
[CoinGecko API](https://www.coingecko.com/en/api)


### Assumptions and Limitations
Lambda environment variable OPENWEATHER_API_KEY must be set.

Cognito hosted UI, using classic UI.

Tokens must be manually retrieved using CLI or custom app.

All components are AWS Free Tier eligible.