# Quick AWS Credential Fix

## The Problem
```
Error: ExpiredToken: The security token included in the request is expired
```

## Quick Solution Steps

### Step 1: Check AWS CLI Installation
```powershell
aws --version
```

If not installed, download from: https://aws.amazon.com/cli/

### Step 2: Reconfigure AWS Credentials
```powershell
aws configure
```

Enter your:
- AWS Access Key ID
- AWS Secret Access Key  
- Default region (e.g., `us-east-1`)
- Default output format (`json`)

### Step 3: Verify Credentials Work
```powershell
aws sts get-caller-identity
```

You should see your account info (not an error).

### Step 4: Run Terraform Again
```powershell
terraform apply
```

## Alternative: Use Environment Variables

If you prefer environment variables, set these in PowerShell:
```powershell
$env:AWS_ACCESS_KEY_ID="your-access-key-id"
$env:AWS_SECRET_ACCESS_KEY="your-secret-access-key"  
$env:AWS_DEFAULT_REGION="us-east-1"
```

## If You Have MFA Enabled

If your AWS account requires MFA, get temporary credentials:
```powershell
aws sts get-session-token --serial-number arn:aws:iam::ACCOUNT-ID:mfa/USERNAME --token-code 123456
```

Then use the temporary credentials returned.

## Common Issues

**Issue**: "aws: command not found"
**Fix**: Install AWS CLI v2 from AWS website

**Issue**: "Invalid credentials" 
**Fix**: Double-check your access keys in AWS IAM console

**Issue**: "Access Denied"
**Fix**: Ensure your AWS user has permissions for Lambda, S3, CloudFront, etc.

---

**Once your AWS credentials are working, run `terraform apply` again!**
