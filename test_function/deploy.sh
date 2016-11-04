#!/bin/bash
cp ../alexa/* ./alexa/
zip -r function.zip alexa/* main.py
aws s3 cp function.zip s3://njsnet-deployments/lambda/Alexa/alexa-lib/ --profile njsnet-sceptre

aws lambda update-function-code --s3-key "lambda/Alexa/alexa-lib/function.zip" --s3-bucket njsnet-deployments --function-name lambda_skill_test --profile njsnet-sceptre --region eu-west-1

