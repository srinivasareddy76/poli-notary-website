# Poli Notary Website - Deployment Guide

## Quick Deployment Steps

### Prerequisites
1. **AWS CLI installed and configured**
   ```bash
   aws configure
   ```

2. **Terraform installed** (version >= 1.0)
   - Download from: https://www.terraform.io/downloads

### Deployment Commands

From the main application directory (`/poli-notary-website`):

#### Option 1: Automated Deployment (Recommended)
```bash
# Make the script executable
chmod +x deploy.sh

# Run the deployment script
./deploy.sh
```

#### Option 2: Manual Deployment
```bash
# Initialize Terraform
terraform init

# Plan the deployment
terraform plan

# Apply the changes
terraform apply
```

### Environment Variables (Optional)
You can customize the deployment by setting these environment variables:

```bash
export AWS_REGION="us-east-1"
export ENVIRONMENT="prod"
export PROJECT_NAME="poli-notary"
```

### Post-Deployment Steps

1. **Verify Email in AWS SES**
   - Go to AWS SES Console
   - Verify your email address for contact form functionality

2. **Test the Website**
   - Visit the CloudFront URL provided in the output
   - Test all forms and functionality

3. **Update DNS (if using custom domain)**
   - Point your domain to the CloudFront distribution

### Deployment Outputs

After successful deployment, you'll get:
- **Website URL**: Your live website URL
- **API Gateway URL**: Backend API endpoint
- **S3 Bucket Name**: Static assets storage
- **CloudFront Distribution ID**: CDN distribution

### File Structure

```
poli-notary-website/
├── index.html              # Main website file
├── styles.css              # Website styles
├── script.js               # Website JavaScript
├── app.py                  # Local development server
├── main.tf                 # Terraform main configuration
├── variables.tf            # Terraform variables
├── outputs.tf              # Terraform outputs
├── deploy.sh               # Deployment script
├── generate_images.py      # Image generation script
├── lambda_functions/       # AWS Lambda functions
│   ├── frontend.py         # Frontend Lambda
│   └── backend.py          # Backend Lambda
└── README.md               # Project documentation
```

### Troubleshooting

#### AWS Credentials Issues
```bash
# Check current AWS configuration
aws sts get-caller-identity

# Reconfigure if needed
aws configure
```

#### Terraform Issues
```bash
# Clean up and reinitialize
rm -rf .terraform
terraform init
```

#### Deployment Cleanup
```bash
# Destroy infrastructure (if needed)
terraform destroy
```

### Cost Estimation
Expected monthly AWS costs:
- Lambda: ~$0.20
- API Gateway: ~$3.50
- CloudFront: ~$1.00
- DynamoDB: ~$1.25
- S3: ~$0.50
- **Total**: ~$6.45/month

### Support
For issues:
1. Check the `AWS_DEPLOYMENT_FIX.md` file
2. Verify AWS credentials and permissions
3. Check CloudWatch logs for errors
4. Ensure all required AWS services are available in your region

---

**Ready to deploy?** Run `./deploy.sh` from this directory!
