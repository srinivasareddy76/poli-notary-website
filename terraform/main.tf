

# Terraform configuration for Poli Notary website using AWS Lambda
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
  }
}

# Configure AWS Provider
provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "poli-notary"
}

variable "environment" {
  description = "Environment"
  type        = string
  default     = "prod"
}

# S3 Bucket for static assets (images, CSS, JS)
resource "aws_s3_bucket" "static_assets" {
  bucket = "${var.project_name}-static-assets-${random_string.bucket_suffix.result}"
}

resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

resource "aws_s3_bucket_public_access_block" "static_assets" {
  bucket = aws_s3_bucket.static_assets.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "static_assets" {
  bucket = aws_s3_bucket.static_assets.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.static_assets.arn}/*"
      }
    ]
  })

  depends_on = [aws_s3_bucket_public_access_block.static_assets]
}

resource "aws_s3_bucket_website_configuration" "static_assets" {
  bucket = aws_s3_bucket.static_assets.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

# DynamoDB table for storing contact form submissions
resource "aws_dynamodb_table" "contact_submissions" {
  name           = "${var.project_name}-contact-submissions"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  global_secondary_index {
    name     = "timestamp-index"
    hash_key = "timestamp"
  }

  tags = {
    Name        = "${var.project_name}-contact-submissions"
    Environment = var.environment
  }
}

# IAM role for Lambda functions
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.project_name}-lambda-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = aws_dynamodb_table.contact_submissions.arn
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "${aws_s3_bucket.static_assets.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "ses:SendEmail",
          "ses:SendRawEmail"
        ]
        Resource = "*"
      }
    ]
  })
}

# Create Lambda deployment packages
data "archive_file" "frontend_lambda_zip" {
  type        = "zip"
  output_path = "${path.module}/frontend_lambda.zip"
  source {
    content = templatefile("${path.module}/lambda_functions/frontend.py", {
      s3_bucket = aws_s3_bucket.static_assets.bucket
    })
    filename = "lambda_function.py"
  }
}

data "archive_file" "backend_lambda_zip" {
  type        = "zip"
  output_path = "${path.module}/backend_lambda.zip"
  source {
    content = templatefile("${path.module}/lambda_functions/backend.py", {
      dynamodb_table = aws_dynamodb_table.contact_submissions.name
    })
    filename = "lambda_function.py"
  }
}

# Frontend Lambda function
resource "aws_lambda_function" "frontend" {
  filename         = data.archive_file.frontend_lambda_zip.output_path
  function_name    = "${var.project_name}-frontend"
  role            = aws_iam_role.lambda_role.arn
  handler         = "lambda_function.lambda_handler"
  runtime         = "python3.9"
  timeout         = 30

  source_code_hash = data.archive_file.frontend_lambda_zip.output_base64sha256

  environment {
    variables = {
      S3_BUCKET = aws_s3_bucket.static_assets.bucket
    }
  }

  tags = {
    Name        = "${var.project_name}-frontend"
    Environment = var.environment
  }
}

# Backend Lambda function
resource "aws_lambda_function" "backend" {
  filename         = data.archive_file.backend_lambda_zip.output_path
  function_name    = "${var.project_name}-backend"
  role            = aws_iam_role.lambda_role.arn
  handler         = "lambda_function.lambda_handler"
  runtime         = "python3.9"
  timeout         = 30

  source_code_hash = data.archive_file.backend_lambda_zip.output_base64sha256

  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.contact_submissions.name
    }
  }

  tags = {
    Name        = "${var.project_name}-backend"
    Environment = var.environment
  }
}

# API Gateway
resource "aws_api_gateway_rest_api" "poli_notary_api" {
  name        = "${var.project_name}-api"
  description = "API for Poli Notary website"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

# API Gateway resources and methods for frontend
resource "aws_api_gateway_resource" "frontend_proxy" {
  rest_api_id = aws_api_gateway_rest_api.poli_notary_api.id
  parent_id   = aws_api_gateway_rest_api.poli_notary_api.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "frontend_proxy" {
  rest_api_id   = aws_api_gateway_rest_api.poli_notary_api.id
  resource_id   = aws_api_gateway_resource.frontend_proxy.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "frontend_root" {
  rest_api_id   = aws_api_gateway_rest_api.poli_notary_api.id
  resource_id   = aws_api_gateway_rest_api.poli_notary_api.root_resource_id
  http_method   = "ANY"
  authorization = "NONE"
}

# API Gateway integration for frontend
resource "aws_api_gateway_integration" "frontend_proxy" {
  rest_api_id = aws_api_gateway_rest_api.poli_notary_api.id
  resource_id = aws_api_gateway_resource.frontend_proxy.id
  http_method = aws_api_gateway_method.frontend_proxy.http_method

  integration_http_method = "POST"
  type                   = "AWS_PROXY"
  uri                    = aws_lambda_function.frontend.invoke_arn
}

resource "aws_api_gateway_integration" "frontend_root" {
  rest_api_id = aws_api_gateway_rest_api.poli_notary_api.id
  resource_id = aws_api_gateway_rest_api.poli_notary_api.root_resource_id
  http_method = aws_api_gateway_method.frontend_root.http_method

  integration_http_method = "POST"
  type                   = "AWS_PROXY"
  uri                    = aws_lambda_function.frontend.invoke_arn
}

# API Gateway resources for backend API
resource "aws_api_gateway_resource" "api" {
  rest_api_id = aws_api_gateway_rest_api.poli_notary_api.id
  parent_id   = aws_api_gateway_rest_api.poli_notary_api.root_resource_id
  path_part   = "api"
}

resource "aws_api_gateway_resource" "contact" {
  rest_api_id = aws_api_gateway_rest_api.poli_notary_api.id
  parent_id   = aws_api_gateway_resource.api.id
  path_part   = "contact"
}

resource "aws_api_gateway_method" "contact_post" {
  rest_api_id   = aws_api_gateway_rest_api.poli_notary_api.id
  resource_id   = aws_api_gateway_resource.contact.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "contact_options" {
  rest_api_id   = aws_api_gateway_rest_api.poli_notary_api.id
  resource_id   = aws_api_gateway_resource.contact.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

# API Gateway integration for backend
resource "aws_api_gateway_integration" "contact_post" {
  rest_api_id = aws_api_gateway_rest_api.poli_notary_api.id
  resource_id = aws_api_gateway_resource.contact.id
  http_method = aws_api_gateway_method.contact_post.http_method

  integration_http_method = "POST"
  type                   = "AWS_PROXY"
  uri                    = aws_lambda_function.backend.invoke_arn
}

resource "aws_api_gateway_integration" "contact_options" {
  rest_api_id = aws_api_gateway_rest_api.poli_notary_api.id
  resource_id = aws_api_gateway_resource.contact.id
  http_method = aws_api_gateway_method.contact_options.http_method

  type = "MOCK"
  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "contact_options" {
  rest_api_id = aws_api_gateway_rest_api.poli_notary_api.id
  resource_id = aws_api_gateway_resource.contact.id
  http_method = aws_api_gateway_method.contact_options.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_integration_response" "contact_options" {
  rest_api_id = aws_api_gateway_rest_api.poli_notary_api.id
  resource_id = aws_api_gateway_resource.contact.id
  http_method = aws_api_gateway_method.contact_options.http_method
  status_code = aws_api_gateway_method_response.contact_options.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
    "method.response.header.Access-Control-Allow-Methods" = "'GET,OPTIONS,POST,PUT'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
}

# Lambda permissions for API Gateway
resource "aws_lambda_permission" "frontend_api_gateway" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.frontend.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.poli_notary_api.execution_arn}/*/*"
}

resource "aws_lambda_permission" "backend_api_gateway" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.backend.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.poli_notary_api.execution_arn}/*/*"
}

# API Gateway deployment
resource "aws_api_gateway_deployment" "poli_notary_deployment" {
  depends_on = [
    aws_api_gateway_integration.frontend_proxy,
    aws_api_gateway_integration.frontend_root,
    aws_api_gateway_integration.contact_post,
    aws_api_gateway_integration.contact_options,
  ]

  rest_api_id = aws_api_gateway_rest_api.poli_notary_api.id
  stage_name  = var.environment

  lifecycle {
    create_before_destroy = true
  }
}

# CloudFront distribution for better performance
resource "aws_cloudfront_distribution" "poli_notary_cdn" {
  origin {
    domain_name = "${aws_api_gateway_rest_api.poli_notary_api.id}.execute-api.${var.aws_region}.amazonaws.com"
    origin_id   = "APIGateway"
    origin_path = "/${var.environment}"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  origin {
    domain_name = aws_s3_bucket.static_assets.bucket_regional_domain_name
    origin_id   = "S3"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.oai.cloudfront_access_identity_path
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods        = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "APIGateway"
    compress               = true
    viewer_protocol_policy = "redirect-to-https"

    forwarded_values {
      query_string = true
      headers      = ["Origin", "Access-Control-Request-Headers", "Access-Control-Request-Method"]
      cookies {
        forward = "none"
      }
    }

    min_ttl     = 0
    default_ttl = 3600
    max_ttl     = 86400
  }

  ordered_cache_behavior {
    path_pattern           = "/assets/*"
    allowed_methods        = ["GET", "HEAD", "OPTIONS"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "S3"
    compress               = true
    viewer_protocol_policy = "redirect-to-https"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    min_ttl     = 0
    default_ttl = 86400
    max_ttl     = 31536000
  }

  price_class = "PriceClass_100"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  tags = {
    Name        = "${var.project_name}-cdn"
    Environment = var.environment
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

resource "aws_cloudfront_origin_access_identity" "oai" {
  comment = "OAI for ${var.project_name}"
}

# Outputs
output "website_url" {
  description = "Website URL"
  value       = "https://${aws_cloudfront_distribution.poli_notary_cdn.domain_name}"
}

output "api_gateway_url" {
  description = "API Gateway URL"
  value       = "https://${aws_api_gateway_rest_api.poli_notary_api.id}.execute-api.${var.aws_region}.amazonaws.com/${var.environment}"
}

output "s3_bucket_name" {
  description = "S3 bucket name for static assets"
  value       = aws_s3_bucket.static_assets.bucket
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID"
  value       = aws_cloudfront_distribution.poli_notary_cdn.id
}

output "dynamodb_table_name" {
  description = "DynamoDB table name"
  value       = aws_dynamodb_table.contact_submissions.name
}

