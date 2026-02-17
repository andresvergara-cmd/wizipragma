# Step 1: Package the SAM/CloudFormation template
aws cloudformation package --s3-bucket your-bucket-name --template-file poc_template.yaml --output-template-file gen2/poc-template.yaml --profile your-profile-name

# Step 2: Deploy the packaged template
aws cloudformation deploy --template-file gen2/poc-template.yaml --stack-name your-stack-name --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM --profile your-profile-name
