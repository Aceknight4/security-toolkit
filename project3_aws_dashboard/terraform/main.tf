# ============================================
# File    : main.tf
# Purpose : AWS Security Dashboard Infrastructure
# Author  : Anel Graph
# Creates : S3 bucket + CloudTrail
# ============================================

# Tell Terraform which cloud provider to use
# and which region to build in
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# -----------------------------------------------
# S3 Bucket — stores all security logs
# -----------------------------------------------
resource "aws_s3_bucket" "security_logs" {
  bucket        = var.bucket_name
  force_destroy = true   # allows terraform destroy to delete bucket

  tags = {
    Name        = "Security Logs"
    Project     = "AWS Security Dashboard"
    Author      = "Anel Graph"
  }
}

# Block all public access — logs must stay private
resource "aws_s3_bucket_public_access_block" "security_logs" {
  bucket = aws_s3_bucket.security_logs.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# -----------------------------------------------
# S3 Bucket Policy — lets CloudTrail write logs
# -----------------------------------------------
resource "aws_s3_bucket_policy" "cloudtrail_policy" {
  bucket = aws_s3_bucket.security_logs.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        # Allow CloudTrail to check the bucket exists
        Sid    = "AWSCloudTrailAclCheck"
        Effect = "Allow"
        Principal = {
          Service = "cloudtrail.amazonaws.com"
        }
        Action   = "s3:GetBucketAcl"
        Resource = aws_s3_bucket.security_logs.arn
      },
      {
        # Allow CloudTrail to write log files
        Sid    = "AWSCloudTrailWrite"
        Effect = "Allow"
        Principal = {
          Service = "cloudtrail.amazonaws.com"
        }
        Action   = "s3:PutObject"
        Resource = "${aws_s3_bucket.security_logs.arn}/cloudtrail/*"
        Condition = {
          StringEquals = {
            "s3:x-amz-acl" = "bucket-owner-full-control"
          }
        }
      }
    ]
  })
}

# -----------------------------------------------
# CloudTrail — records every AWS API call
# -----------------------------------------------
resource "aws_cloudtrail" "security_trail" {
  name                          = var.trail_name
  s3_bucket_name                = aws_s3_bucket.security_logs.id
  s3_key_prefix                 = "cloudtrail"
  include_global_service_events = true
  is_multi_region_trail         = false
  enable_logging                = true

  tags = {
    Name    = "Security Trail"
    Project = "AWS Security Dashboard"
  }

  # CloudTrail needs the bucket policy first
  depends_on = [aws_s3_bucket_policy.cloudtrail_policy]
}
