# ============================================
# File    : variables.tf
# Purpose : Configurable values for main.tf
# ============================================

variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "eu-north-1"
}

variable "bucket_name" {
  description = "S3 bucket name — must be globally unique"
  type        = string
  default     = "anel-security-logs-185188589088"
}

variable "trail_name" {
  description = "CloudTrail trail name"
  type        = string
  default     = "anel-security-trail"
}
