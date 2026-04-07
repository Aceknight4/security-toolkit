# ============================================
# File    : outputs.tf
# Purpose : Print useful info after terraform apply
# ============================================

output "bucket_name" {
  description = "S3 bucket storing security logs"
  value       = aws_s3_bucket.security_logs.id
}

output "bucket_arn" {
  description = "S3 bucket ARN"
  value       = aws_s3_bucket.security_logs.arn
}

output "cloudtrail_name" {
  description = "CloudTrail trail name"
  value       = aws_cloudtrail.security_trail.name
}

output "cloudtrail_arn" {
  description = "CloudTrail trail ARN"
  value       = aws_cloudtrail.security_trail.arn
}
