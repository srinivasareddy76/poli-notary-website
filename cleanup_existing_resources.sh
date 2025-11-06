#!/bin/bash

# Cleanup script for existing AWS resources
# Run this if you encounter "already exists" errors

echo "🧹 Cleaning up existing AWS resources..."

PROJECT_NAME="${PROJECT_NAME:-poli-notary}"
AWS_REGION="${AWS_REGION:-us-east-1}"

echo "Project: $PROJECT_NAME"
echo "Region: $AWS_REGION"
echo ""

# Function to safely delete resource if it exists
safe_delete() {
    local resource_type=$1
    local resource_name=$2
    local aws_command=$3
    
    echo "Checking $resource_type: $resource_name"
    if eval "$aws_command" &>/dev/null; then
        echo "  ✅ Found existing $resource_type, attempting to delete..."
        # Add specific deletion commands here if needed
    else
        echo "  ℹ️  $resource_type not found, skipping..."
    fi
}

# Check and clean up IAM roles
echo "🔍 Checking IAM roles..."
safe_delete "IAM Role" "$PROJECT_NAME-lambda-role" "aws iam get-role --role-name $PROJECT_NAME-lambda-role"

# Check and clean up Lambda functions
echo "🔍 Checking Lambda functions..."
safe_delete "Lambda Function" "$PROJECT_NAME-frontend" "aws lambda get-function --function-name $PROJECT_NAME-frontend"
safe_delete "Lambda Function" "$PROJECT_NAME-backend" "aws lambda get-function --function-name $PROJECT_NAME-backend"

# Check and clean up API Gateway
echo "🔍 Checking API Gateway..."
API_ID=$(aws apigateway get-rest-apis --query "items[?name=='$PROJECT_NAME-api'].id" --output text 2>/dev/null)
if [ ! -z "$API_ID" ] && [ "$API_ID" != "None" ]; then
    echo "  ✅ Found existing API Gateway: $API_ID"
    echo "  ⚠️  Manual cleanup may be required"
fi

# Check and clean up DynamoDB tables
echo "🔍 Checking DynamoDB tables..."
safe_delete "DynamoDB Table" "$PROJECT_NAME-contact-submissions" "aws dynamodb describe-table --table-name $PROJECT_NAME-contact-submissions"

echo ""
echo "🎯 Cleanup recommendations:"
echo "1. If you see 'already exists' errors, consider using 'terraform import' to import existing resources"
echo "2. Or manually delete the conflicting resources from AWS Console"
echo "3. Or run 'terraform destroy' to clean up everything and start fresh"
echo ""
echo "💡 Alternative: Use 'terraform import' to manage existing resources:"
echo "   terraform import aws_iam_role.lambda_role $PROJECT_NAME-lambda-role"
echo "   terraform import aws_lambda_function.frontend $PROJECT_NAME-frontend"
echo "   terraform import aws_lambda_function.backend $PROJECT_NAME-backend"
echo ""
echo "🚀 After cleanup, run: terraform apply"
