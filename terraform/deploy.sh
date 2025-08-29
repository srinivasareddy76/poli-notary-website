


#!/bin/bash

# Deployment script for Poli Notary website on AWS Lambda
set -e

echo "🚀 Deploying Poli Notary website to AWS Lambda..."

# Check if Terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform is not installed. Please install Terraform first."
    exit 1
fi

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS CLI is not configured. Please run 'aws configure' first."
    exit 1
fi

# Set variables
PROJECT_NAME="poli-notary"
AWS_REGION="${AWS_REGION:-us-east-1}"
ENVIRONMENT="${ENVIRONMENT:-prod}"

echo "📋 Deployment Configuration:"
echo "  • Project: $PROJECT_NAME"
echo "  • Region: $AWS_REGION"
echo "  • Environment: $ENVIRONMENT"
echo ""

# Initialize Terraform
echo "🔧 Initializing Terraform..."
terraform init

# Validate Terraform configuration
echo "✅ Validating Terraform configuration..."
terraform validate

# Plan deployment
echo "📋 Planning deployment..."
terraform plan \
    -var="aws_region=$AWS_REGION" \
    -var="project_name=$PROJECT_NAME" \
    -var="environment=$ENVIRONMENT" \
    -out=tfplan

# Ask for confirmation
echo ""
read -p "🤔 Do you want to proceed with the deployment? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Apply Terraform configuration
    echo "🚀 Deploying infrastructure..."
    terraform apply tfplan
    
    # Get outputs
    echo ""
    echo "📊 Deployment Results:"
    echo "  • Website URL: $(terraform output -raw website_url)"
    echo "  • API Gateway URL: $(terraform output -raw api_gateway_url)"
    echo "  • S3 Bucket: $(terraform output -raw s3_bucket_name)"
    echo "  • CloudFront Distribution: $(terraform output -raw cloudfront_distribution_id)"
    echo ""
    
    # Generate and upload images
    echo "🎨 Generating and uploading website images..."
    S3_BUCKET=$(terraform output -raw s3_bucket_name) python3 generate_images.py
    
    # Invalidate CloudFront cache
    CLOUDFRONT_ID=$(terraform output -raw cloudfront_distribution_id)
    echo "🔄 Invalidating CloudFront cache..."
    aws cloudfront create-invalidation \
        --distribution-id "$CLOUDFRONT_ID" \
        --paths "/*" \
        --region "$AWS_REGION"
    
    echo ""
    echo "✅ Deployment completed successfully!"
    echo ""
    echo "🌐 Your Poli Notary website is now live at:"
    echo "   $(terraform output -raw website_url)"
    echo ""
    echo "📝 Next Steps:"
    echo "  1. Verify email addresses in AWS SES for contact form functionality"
    echo "  2. Update DNS records if using a custom domain"
    echo "  3. Test all website functionality"
    echo "  4. Monitor CloudWatch logs for any issues"
    echo ""
    
else
    echo "❌ Deployment cancelled."
    rm -f tfplan
    exit 1
fi

# Clean up
rm -f tfplan

echo "🎉 Deployment script completed!"


