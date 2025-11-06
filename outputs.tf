




# Outputs for Poli Notary Terraform deployment

output "website_url" {
  description = "URL of the deployed website"
  value       = var.domain_name != "" ? "https://${var.domain_name}" : "https://${aws_cloudfront_distribution.poli_notary_cdn.domain_name}"
}

output "cloudfront_domain_name" {
  description = "CloudFront distribution domain name"
  value       = aws_cloudfront_distribution.poli_notary_cdn.domain_name
}

output "api_gateway_url" {
  description = "API Gateway URL"
  value       = "https://${aws_api_gateway_rest_api.poli_notary_api.id}.execute-api.${var.aws_region}.amazonaws.com/${var.environment}"
}

output "api_gateway_id" {
  description = "API Gateway ID"
  value       = aws_api_gateway_rest_api.poli_notary_api.id
}

output "s3_bucket_name" {
  description = "S3 bucket name for static assets"
  value       = aws_s3_bucket.static_assets.bucket
}

output "s3_bucket_website_endpoint" {
  description = "S3 bucket website endpoint"
  value       = aws_s3_bucket_website_configuration.static_assets.website_endpoint
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID"
  value       = aws_cloudfront_distribution.poli_notary_cdn.id
}

output "cloudfront_distribution_arn" {
  description = "CloudFront distribution ARN"
  value       = aws_cloudfront_distribution.poli_notary_cdn.arn
}

output "dynamodb_table_name" {
  description = "DynamoDB table name for contact submissions"
  value       = aws_dynamodb_table.contact_submissions.name
}

output "dynamodb_table_arn" {
  description = "DynamoDB table ARN"
  value       = aws_dynamodb_table.contact_submissions.arn
}

output "frontend_lambda_function_name" {
  description = "Frontend Lambda function name"
  value       = aws_lambda_function.frontend.function_name
}

output "frontend_lambda_function_arn" {
  description = "Frontend Lambda function ARN"
  value       = aws_lambda_function.frontend.arn
}

output "backend_lambda_function_name" {
  description = "Backend Lambda function name"
  value       = aws_lambda_function.backend.function_name
}

output "backend_lambda_function_arn" {
  description = "Backend Lambda function ARN"
  value       = aws_lambda_function.backend.arn
}

output "lambda_role_arn" {
  description = "IAM role ARN for Lambda functions"
  value       = aws_iam_role.lambda_role.arn
}

output "deployment_info" {
  description = "Deployment information summary"
  value = {
    project_name    = var.project_name
    environment     = var.environment
    aws_region      = var.aws_region
    deployment_time = timestamp()
  }
}

output "next_steps" {
  description = "Next steps after deployment"
  value = [
    "1. Verify email addresses in AWS SES console for contact form functionality",
    "2. Test the website functionality at the provided URL",
    "3. Update DNS records if using a custom domain",
    "4. Monitor CloudWatch logs for any issues",
    "5. Set up monitoring and alerts as needed",
    "6. Configure backup and disaster recovery procedures"
  ]
}

output "important_notes" {
  description = "Important notes about the deployment"
  value = [
    "• Contact form emails require verified SES email addresses",
    "• CloudFront distribution may take 15-20 minutes to fully deploy",
    "• DynamoDB table uses on-demand billing for cost optimization",
    "• Lambda functions are configured with appropriate IAM permissions",
    "• All resources are tagged for easy identification and cost tracking"
  ]
}

output "monitoring_urls" {
  description = "URLs for monitoring and management"
  value = {
    cloudwatch_logs     = "https://${var.aws_region}.console.aws.amazon.com/cloudwatch/home?region=${var.aws_region}#logsV2:log-groups"
    dynamodb_console    = "https://${var.aws_region}.console.aws.amazon.com/dynamodbv2/home?region=${var.aws_region}#table?name=${aws_dynamodb_table.contact_submissions.name}"
    lambda_console      = "https://${var.aws_region}.console.aws.amazon.com/lambda/home?region=${var.aws_region}#/functions"
    cloudfront_console  = "https://console.aws.amazon.com/cloudfront/v3/home#/distributions/${aws_cloudfront_distribution.poli_notary_cdn.id}"
    s3_console         = "https://s3.console.aws.amazon.com/s3/buckets/${aws_s3_bucket.static_assets.bucket}"
  }
}

output "cost_optimization_tips" {
  description = "Tips for optimizing AWS costs"
  value = [
    "• DynamoDB is configured with on-demand billing - monitor usage",
    "• Lambda functions have appropriate memory allocation",
    "• CloudFront caching is optimized for static assets",
    "• S3 lifecycle policies can be added for long-term cost savings",
    "• Consider using AWS Cost Explorer to monitor spending"
  ]
}




