






# Poli Notary Website - AWS Lambda Deployment

This Terraform configuration deploys a professional website for Poli Notary using AWS Lambda, API Gateway, CloudFront, and other AWS services for a scalable, cost-effective solution.

## 🏗️ Architecture Overview

The deployment creates a serverless architecture with the following components:

- **Frontend Lambda**: Serves the HTML, CSS, and JavaScript
- **Backend Lambda**: Handles contact form submissions and API requests
- **API Gateway**: Routes requests to appropriate Lambda functions
- **CloudFront**: CDN for global content delivery and caching
- **S3 Bucket**: Stores static assets (images, documents)
- **DynamoDB**: Stores contact form submissions
- **SES**: Sends notification and confirmation emails
- **IAM Roles**: Secure access control for all services

## 📋 Prerequisites

Before deploying, ensure you have:

1. **AWS CLI** installed and configured
   ```bash
   aws configure
   ```

2. **Terraform** installed (version >= 1.0)
   ```bash
   # On macOS
   brew install terraform
   
   # On Ubuntu/Debian
   sudo apt-get install terraform
   
   # On Windows
   choco install terraform
   ```

3. **Python 3** with PIL (Pillow) for image generation
   ```bash
   pip install Pillow boto3
   ```

4. **Appropriate AWS permissions** for:
   - Lambda functions
   - API Gateway
   - CloudFront
   - S3 buckets
   - DynamoDB
   - IAM roles and policies
   - SES (for email functionality)

## 🚀 Quick Deployment

### Option 1: Using the Deployment Script (Recommended)

```bash
# Make the script executable
chmod +x deploy.sh

# Run the deployment
./deploy.sh
```

### Option 2: Manual Deployment

```bash
# Initialize Terraform
terraform init

# Plan the deployment
terraform plan -var="project_name=poli-notary" -var="aws_region=us-east-1"

# Apply the configuration
terraform apply

# Generate and upload images
S3_BUCKET=$(terraform output -raw s3_bucket_name) python3 generate_images.py
```

## ⚙️ Configuration Options

### Basic Configuration

```bash
# Set environment variables
export AWS_REGION="us-east-1"
export ENVIRONMENT="prod"
export PROJECT_NAME="poli-notary"

# Deploy with custom variables
terraform apply \
  -var="aws_region=$AWS_REGION" \
  -var="project_name=$PROJECT_NAME" \
  -var="environment=$ENVIRONMENT"
```

### Advanced Configuration

Create a `terraform.tfvars` file:

```hcl
# terraform.tfvars
aws_region = "us-east-1"
project_name = "poli-notary"
environment = "prod"

# Custom domain (optional)
domain_name = "www.polinotary.com"
certificate_arn = "arn:aws:acm:us-east-1:123456789012:certificate/12345678-1234-1234-1234-123456789012"

# Business information
notification_email = "info@polinotary.com"
business_phone = "(555) 123-4567"
business_email = "info@polinotary.com"
service_area = "Greater Los Angeles Area"

# Performance settings
lambda_timeout = 30
lambda_memory_size = 256
cloudfront_price_class = "PriceClass_100"

# Security and compliance
enable_waf = true
enable_ses_email = true

# Additional tags
tags = {
  Project = "Poli Notary Website"
  Owner = "Poli Notary"
  Environment = "Production"
  ManagedBy = "Terraform"
}
```

## 📧 Email Configuration

To enable contact form email functionality:

1. **Verify email addresses in SES**:
   ```bash
   # Verify the sender email
   aws ses verify-email-identity --email-address info@polinotary.com
   
   # Verify the notification recipient email
   aws ses verify-email-identity --email-address your-email@example.com
   ```

2. **Check verification status**:
   ```bash
   aws ses get-identity-verification-attributes --identities info@polinotary.com
   ```

3. **Request production access** (if needed):
   - Go to AWS SES Console
   - Request to move out of sandbox mode
   - This allows sending to unverified email addresses

## 🎨 Image Management

The deployment includes professional placeholder images. To customize:

### Generate New Images

```bash
# Set your S3 bucket name
export S3_BUCKET="your-bucket-name"

# Generate and upload images
python3 generate_images.py
```

### Upload Custom Images

```bash
# Upload your own images to S3
aws s3 cp your-image.jpg s3://your-bucket-name/assets/images/
aws s3 cp another-image.jpg s3://your-bucket-name/assets/images/

# Make them publicly readable
aws s3api put-object-acl --bucket your-bucket-name --key assets/images/your-image.jpg --acl public-read
```

### Image Specifications

| Image | Size | Purpose |
|-------|------|---------|
| `notary-professional.jpg` | 600x400 | Hero section |
| `document-signing.jpg` | 400x300 | Services section |
| `real-estate.jpg` | 400x300 | Services section |
| `mobile-service.jpg` | 400x300 | Services section |
| `business-documents.jpg` | 400x300 | Services section |
| `notary-portrait.jpg` | 400x500 | About section |
| `client-1.jpg` | 150x150 | Testimonials |
| `client-2.jpg` | 150x150 | Testimonials |
| `client-3.jpg` | 150x150 | Testimonials |

## 🔧 Customization

### Update Business Information

Edit the Lambda function templates in `lambda_functions/frontend.py`:

```python
# Update contact information
phone_number = "(555) 123-4567"
email_address = "info@polinotary.com"
service_area = "Your Service Area"
```

### Modify Website Content

The website content is embedded in the frontend Lambda function. Key sections to customize:

1. **Hero Section**: Update headline and value proposition
2. **Services**: Modify service offerings and descriptions
3. **About Section**: Update credentials and experience
4. **Testimonials**: Replace with real client testimonials
5. **Contact Information**: Update all contact details

### Styling Changes

CSS is served from the frontend Lambda. Modify the `serve_css()` function in `frontend.py` to update:

- Colors and branding
- Typography
- Layout and spacing
- Responsive breakpoints

## 📊 Monitoring and Maintenance

### CloudWatch Logs

Monitor Lambda function logs:

```bash
# View frontend logs
aws logs tail /aws/lambda/poli-notary-frontend --follow

# View backend logs
aws logs tail /aws/lambda/poli-notary-backend --follow
```

### DynamoDB Data

View contact form submissions:

```bash
# Scan the DynamoDB table
aws dynamodb scan --table-name poli-notary-contact-submissions
```

### CloudFront Cache Management

```bash
# Invalidate cache after updates
aws cloudfront create-invalidation \
  --distribution-id YOUR_DISTRIBUTION_ID \
  --paths "/*"
```

## 💰 Cost Optimization

### Expected Monthly Costs (Low Traffic)

- **Lambda**: ~$0.20 (1M requests)
- **API Gateway**: ~$3.50 (1M requests)
- **CloudFront**: ~$1.00 (10GB transfer)
- **DynamoDB**: ~$1.25 (on-demand)
- **S3**: ~$0.50 (storage + requests)
- **Total**: ~$6.45/month

### Cost Optimization Tips

1. **Use CloudFront caching** effectively
2. **Monitor DynamoDB usage** (on-demand billing)
3. **Set up S3 lifecycle policies** for old assets
4. **Use AWS Cost Explorer** for detailed analysis
5. **Consider Reserved Capacity** for predictable workloads

## 🔒 Security Features

- **HTTPS everywhere** via CloudFront
- **CORS protection** on API endpoints
- **IAM least privilege** access
- **Input validation** on forms
- **Rate limiting** via API Gateway
- **WAF protection** (optional)

## 🚨 Troubleshooting

### Common Issues

1. **Email not sending**:
   - Verify SES email addresses
   - Check SES sandbox status
   - Review Lambda logs for errors

2. **Images not loading**:
   - Verify S3 bucket permissions
   - Check CloudFront cache status
   - Ensure images are publicly readable

3. **Form submissions failing**:
   - Check DynamoDB permissions
   - Review API Gateway logs
   - Verify CORS configuration

4. **Website not accessible**:
   - Check CloudFront distribution status
   - Verify Lambda function deployment
   - Review API Gateway configuration

### Debug Commands

```bash
# Check Lambda function status
aws lambda get-function --function-name poli-notary-frontend

# Test API Gateway endpoint
curl -X POST https://your-api-id.execute-api.region.amazonaws.com/prod/api/contact \
  -H "Content-Type: application/json" \
  -d '{"fullName":"Test","email":"test@example.com","phone":"555-1234","serviceType":"standard"}'

# Check CloudFront distribution
aws cloudfront get-distribution --id YOUR_DISTRIBUTION_ID
```

## 🔄 Updates and Maintenance

### Updating the Website

1. **Modify the code** in `lambda_functions/`
2. **Run Terraform apply** to deploy changes
3. **Invalidate CloudFront cache** if needed

```bash
# Update and deploy
terraform apply

# Invalidate cache
aws cloudfront create-invalidation \
  --distribution-id $(terraform output -raw cloudfront_distribution_id) \
  --paths "/*"
```

### Backup and Recovery

- **DynamoDB**: Point-in-time recovery enabled
- **S3**: Versioning can be enabled
- **Lambda**: Code is stored in Terraform state
- **Infrastructure**: Terraform state should be backed up

## 📞 Support

For issues with this deployment:

1. Check the troubleshooting section above
2. Review AWS CloudWatch logs
3. Consult AWS documentation
4. Consider AWS Support if needed

## 📄 License

This Terraform configuration is provided as-is for the Poli Notary website deployment. Modify as needed for your specific requirements.

---

**Note**: Remember to customize all placeholder content, contact information, and branding to match your actual business details before going live.






