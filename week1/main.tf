terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "eu-north-1"
}

resource "aws_s3_bucket" "bucket" {
  bucket = "my-de-zoomer-bucket"

  tags = {
    Name        = "DE Bucket"
    Environment = "Dev"
  }

  force_destroy = true

}

resource "aws_s3_bucket_lifecycle_configuration" "bucket-config" {
  bucket = aws_s3_bucket.bucket.id

  rule {
    id = "rule-1"

    expiration {
      days = 1
    }
    abort_incomplete_multipart_upload {
      days_after_initiation = 1
    }
    status = "Enabled"
  }

}

resource "aws_redshift_cluster" "cluster" {
  cluster_identifier = var.redshift_cluster_name
  database_name      = var.redshift_db_name
  master_username    = "de_zoomer"
  master_password    = var.master_password
  node_type          = "dc2.large"
  cluster_type       = "single-node"
  # Skips snapshot on deletion, use with care
  skip_final_snapshot = true
}

