



# Variables for Poli Notary Terraform configuration

variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
  
  validation {
    condition = can(regex("^[a-z0-9-]+$", var.aws_region))
    error_message = "AWS region must be a valid region identifier."
  }
}

variable "project_name" {
  description = "Name of the project (used for resource naming)"
  type        = string
  default     = "poli-notary"
  
  validation {
    condition = can(regex("^[a-z0-9-]+$", var.project_name))
    error_message = "Project name must contain only lowercase letters, numbers, and hyphens."
  }
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "prod"
  
  validation {
    condition = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

variable "domain_name" {
  description = "Custom domain name for the website (optional)"
  type        = string
  default     = ""
}

variable "certificate_arn" {
  description = "ARN of SSL certificate for custom domain (required if domain_name is set)"
  type        = string
  default     = ""
}

variable "notification_email" {
  description = "Email address to receive contact form notifications"
  type        = string
  default     = "info@polinotary.com"
  
  validation {
    condition = can(regex("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$", var.notification_email))
    error_message = "Notification email must be a valid email address."
  }
}

variable "business_phone" {
  description = "Business phone number"
  type        = string
  default     = "(555) 123-4567"
}

variable "business_email" {
  description = "Business email address"
  type        = string
  default     = "info@polinotary.com"
}

variable "service_area" {
  description = "Service area description"
  type        = string
  default     = "Greater Metropolitan Area"
}

variable "enable_ses_email" {
  description = "Enable SES email functionality (requires verified email addresses)"
  type        = bool
  default     = false
}

variable "lambda_timeout" {
  description = "Timeout for Lambda functions in seconds"
  type        = number
  default     = 30
  
  validation {
    condition = var.lambda_timeout >= 3 && var.lambda_timeout <= 900
    error_message = "Lambda timeout must be between 3 and 900 seconds."
  }
}

variable "lambda_memory_size" {
  description = "Memory size for Lambda functions in MB"
  type        = number
  default     = 256
  
  validation {
    condition = var.lambda_memory_size >= 128 && var.lambda_memory_size <= 10240
    error_message = "Lambda memory size must be between 128 and 10240 MB."
  }
}

variable "cloudfront_price_class" {
  description = "CloudFront price class"
  type        = string
  default     = "PriceClass_100"
  
  validation {
    condition = contains(["PriceClass_All", "PriceClass_200", "PriceClass_100"], var.cloudfront_price_class)
    error_message = "CloudFront price class must be one of: PriceClass_All, PriceClass_200, PriceClass_100."
  }
}

variable "enable_waf" {
  description = "Enable AWS WAF for additional security"
  type        = bool
  default     = false
}

variable "backup_retention_days" {
  description = "Number of days to retain DynamoDB backups"
  type        = number
  default     = 30
  
  validation {
    condition = var.backup_retention_days >= 1 && var.backup_retention_days <= 35
    error_message = "Backup retention days must be between 1 and 35."
  }
}

variable "tags" {
  description = "Additional tags to apply to all resources"
  type        = map(string)
  default = {
    Project     = "Poli Notary Website"
    ManagedBy   = "Terraform"
    Owner       = "Poli Notary"
  }
}



