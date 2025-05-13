# 🌐 AWS API Gateway with Cognito Authentication and Lambda Integration

## 📌 Overview

This project demonstrates an AWS-based REST API with secure Cognito authentication and two Lambda functions integrating public APIs (OpenWeather and CoinGecko).

---

## 🔧 Architecture

- **Amazon Cognito** – Handles user authentication.
- **API Gateway** – Exposes RESTful endpoints secured by Cognito.
- **Lambda Functions** – Call:
  - 🌦️ OpenWeatherMap API (Node.js)
  - 📈 CoinGecko API (Python)
- **CloudFormation** – Manages infrastructure-as-code.

---

## 📁 Repository Structure
```plaintext
/aws-api-gateway-assessment
├── README.md
├── cloudformation
│   └── main.yaml
├── lambdas
│   ├── lambda1/index.mjs
│   ├── lambda2/lambda_function.py
└── assets/
```

---

## 🚀 Deployment Instructions

### 1️⃣ Prerequisites
- ✅ AWS CLI and access credentials
- ✅ S3 bucket (name: `aws-api-gateway-assessment`) to upload Lambda code

---

### 2️⃣ Steps

#### 📁 Zip and Upload Lambda Functions
1. Install dependencies for Node.js:
   ```bash
   cd /lambdas/lambda1
   npm install node-fetch
   ```
2. Package dependencies into zip files.  
   Refer to:
   - [Build Node.js .zip file](https://docs.aws.amazon.com/lambda/latest/dg/nodejs-package.html#nodejs-package-create-dependencies)
   - [Build Python .zip file](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-create-dependencies)
3. Upload zip files using AWS Console or AWS CLI:
   ```bash
   aws s3 cp lambda1.zip s3://aws-api-gateway-assessment/lambda1.zip 
   aws s3 cp lambda2.zip s3://aws-api-gateway-assessment/lambda2.zip
   ```

#### 🛫 Deploy CloudFormation
Deploy the CloudFormation stack:
   ```bash
   aws cloudformation deploy \
       --template-file cloudformation/main.yaml \
       --stack-name api-cognito-demo \
       --capabilities CAPABILITY_NAMED_IAM \
       --parameter-overrides \
       Lambda1S3Key=lambda1.zip \
       Lambda2S3Key=lambda2.zip
   ```

#### 🔑 Set Up Environment Variables for Node.js Lambda Function
Set the required environment variable:
   ```bash
   OPENWEATHER_API_KEY=<your_api_key>
   ```

#### 📜 Note Outputs
After deployment, note the following outputs:
```plaintext
- API URL: your_api_url
- UserPool ID: your_userpool_id
- Cognito Domain: your_domain_url
- App Client ID/Secrets: your_app_client_id, your_app_client_secret
```

---

### 3️⃣ Cognito Setup

#### 🧑‍💻 Sign Up a User
1. Go to **Cognito > User Pools > `ApiGatewayUserPool`**.
2. Create a test user with:
   - Username: `test_username`
   - Temporary Password: `temporary_password`

---

### 4️⃣ Testing with Postman

#### 🔐 Authenticate and Get Token
1. In Postman, go to `<your_collection>/<your_request>` pane.
2. Under the **Authorization** tab, choose **OAuth 2.0**.
3. Configure a new token with the following details:
   ```plaintext
   Callback URL: http://localhost:8080/
   Auth URL: <your_domain_url>/oauth2/authorize
   Access Token URL: <your_domain_url>/oauth2/token
   Client ID: <your_app_client_id>
   Client Secret: <your_app_client_secret>
   ```
4. Log in with `test_username` and `temporary_password`, then click **Get New Access Token**.
5. Note the ID token.

#### 🌐 Test API Endpoints
1. In Postman, set the headers:  
   ```json
   { "Authorization": "<your_id_token>" }
   ```
2. Test the endpoints:
   - **GET** `<your_api_url>/weather`  
     Example output:
     ```json
     {
         "city": "Toronto",
         "temperature": 13.84,
         "weather": "overcast clouds"
     }
     ```
   - **POST** `<your_api_url>/crypto`  
     Example output:
     ```json
     {
         "coin": "bitcoin",
         "currency": "usd",
         "price": 102371
     }
     ```

---

## 🌐 External Services Used
- 🌦️ [OpenWeatherMap API](https://openweathermap.org/api)  
- 📈 [CoinGecko API](https://www.coingecko.com/en/api)

---

## 🛠️ Assumptions and Limitations
- 🔑 Lambda environment variable `OPENWEATHER_API_KEY` must be set.
- 🖥️ Cognito hosted UI uses the classic UI.
- 🧑‍💻 Tokens must be manually retrieved using CLI or a custom app.
- 🆓 All components are AWS Free Tier eligible.