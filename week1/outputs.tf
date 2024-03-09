output "redshift_cluster_availability_zone" {
  value       = aws_redshift_cluster.cluster.availability_zone
  description = "The availability zone where the Redshift cluster is deployed."
}

