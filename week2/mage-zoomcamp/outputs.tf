output "redshift_cluster_id" {
  value       = aws_redshift_cluster.cluster.cluster_identifier
  description = "The ID of the Redshift cluster"
}
