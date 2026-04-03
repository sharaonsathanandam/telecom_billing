variable "project" {
  description = "The Google Cloud project ID."
}

variable "code_bucket" {
  description = "Name of the gcs bucket for storing python programs"
}

variable "logs_bucket" {
  description = "Name of the gcs bucket for storing logs"
}

variable "stage_data_bucket" {
  description = "Name of the gcs bucket for storing stage data"
}

variable "current_data_folder" {
  description = "Name of the gcs bucket folder for storing current data"
}

variable "archive_data_folder" {
  description = "Name of the gcs bucket folder for storing archived data"
}

variable "logs_temp_folder" {
  description = "Name of the gcs bucket folder for storing logs temp data"
}