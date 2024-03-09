variable "credentials" {
  description = "My Credentials"
  default     = "./keys/my-creds.json"
}

variable "redshift_cluster_name" {
  description = "Redshift Cluster Name"
  default     = "de-zoomer-cluster"
}

variable "redshift_db_name" {
  description = "Redshift DB Name"
  default     = "de_zoomer_rs_db"
}

variable "master_password" {
  description = "Redshift Master Password"
}
