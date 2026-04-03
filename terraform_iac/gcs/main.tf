resource "google_storage_bucket" "code_bucket" {
  name     = var.code_bucket
  location = "US"
  force_destroy = true
  public_access_prevention = "enforced"
  project = var.project
}

resource "google_storage_bucket" "logs_bucket" {
  name     = var.logs_bucket
  location = "US"
  force_destroy = true
  public_access_prevention = "enforced"
  project = var.project
}

resource "google_storage_bucket" "stage_data_bucket" {
  name     = var.stage_data_bucket
  location = "US"
  force_destroy = true
  public_access_prevention = "enforced"
  project = var.project
}

resource "google_storage_bucket_object" "current_data_folder" {
  name   = var.current_data_folder
  bucket = google_storage_bucket.stage_data_bucket.name
  content = " "
}

resource "google_storage_bucket_object" "archive_data_folder" {
  name   = var.archive_data_folder
  bucket = google_storage_bucket.stage_data_bucket.name
  content = " "
}

resource "google_storage_bucket_object" "logs_temp_folder" {
  name   = var.logs_temp_folder
  bucket = google_storage_bucket.logs_bucket.name
  content = " "
}
