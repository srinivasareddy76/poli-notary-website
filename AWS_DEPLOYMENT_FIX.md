# AWS Deployment Fix Guide

## Problem
Your Terraform deployment is failing with the error:
```
Error: ExpiredToken: The security token included in the request is expired
```

## Solution Steps

### 1. Check AWS CLI Installation
First, ensure AWS CLI is installed on your local machine:
```bash
aws --version
```

If not installed, install it:
- **Windows**: Download from https://aws.amazon.com/cli/
- **macOS**: `brew install awscli` or download installer
- **Linux**: `sudo apt install awscli` or `sudo yum install awscli`

### 2. Reconfigure AWS Credentials
Run the following command to reconfigure your AWS credentials:
```bash
aws configure
```

You'll be prompted to enter:
- **AWS Access Key ID**: Your access key
- **AWS Secret Access Key**: Your secret key
- **Default region name**: e.g., `us-east-1`
- **Default output format**: `json`

### 3. Alternative: Use Environment Variables
If you prefer environment variables, set these in your terminal:
```bash
export AWS_ACCESS_KEY_ID="your-access-key-id"
export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
export AWS_DEFAULT_REGION="us-east-1"
```

### 4. Verify AWS Configuration
Test your credentials:
```bash
aws sts get-caller-identity
```

You should see output like:
```json
{
    "UserId": "AIDACKCEVSQ6C2EXAMPLE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/your-username"
}
```

### 5. Deploy with Terraform
Once AWS credentials are working, run the deployment from the main application directory:
```bash
# Using the deployment script (recommended)
./deploy.sh
```

Or manually:
```bash
# Manual deployment
terraform init
terraform plan
terraform apply
```

## Common Issues & Solutions

### Issue 1: AWS CLI Not Found
**Solution**: Install AWS CLI v2 from the official AWS website

### Issue 2: Invalid Credentials
**Solution**: 
- Check if your AWS access keys are correct
- Ensure your AWS account has necessary permissions
- Verify the keys haven't been rotated or disabled

### Issue 3: Region Mismatch
**Solution**: 
- Ensure your AWS region matches the one in terraform variables
- Set the correct region in `aws configure` or environment variables

### Issue 4: Permission Denied
**Solution**: 
- Your AWS user needs permissions for:
  - Lambda functions
  - API Gateway
  - S3 buckets
  - CloudFront
  - DynamoDB
  - SES (Simple Email Service)
  - IAM roles

### Issue 5: MFA Required
If your AWS account requires MFA, you'll need to use temporary credentials:
```bash
aws sts get-session-token --serial-number arn:aws:iam::123456789012:mfa/your-username --token-code 123456
```

Then use the temporary credentials returned.

## Terraform Variables
Make sure to set these variables in `terraform/terraform.tfvars`:
```hcl
aws_region = "us-east-1"
project_name = "poli-notary"
environment = "prod"
```

## Next Steps After Successful Deployment
1. **Verify Email in SES**: Go to AWS SES console and verify your email address
2. **Test the Website**: Visit the CloudFront URL provided in the output
3. **Update DNS**: Point your domain to the CloudFront distribution
4. **Monitor Logs**: Check CloudWatch logs for any issues

## Cost Estimation
Expected monthly costs for the AWS infrastructure:
- Lambda: ~$0.20
- API Gateway: ~$3.50
- CloudFront: ~$1.00
- DynamoDB: ~$1.25
- S3: ~$0.50
- **Total**: ~$6.45/month

## Support
If you continue to have issues:
1. Check AWS CloudTrail for detailed error logs
2. Verify all required AWS services are available in your region
3. Ensure your AWS account is in good standing
4. Contact AWS support if needed

The deployment should work once your AWS credentials are properly configured!
