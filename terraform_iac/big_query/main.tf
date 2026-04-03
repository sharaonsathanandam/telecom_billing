resource "google_bigquery_dataset" "mobile-usage-dataset" {
  dataset_id                 = "sharaon_mobile_usage"
  project                    = var.project
  location                   = "US"  # Replace with your desired location
  deletion_protection        = false
}

resource "google_bigquery_table" "table" {
  dataset_id = google_bigquery_dataset.mobile-usage-dataset.dataset_id
  table_id   = "mobile_usage_data"
  project    = var.project
  deletion_protection=false
  schema = <<EOF
  [
    {"name": "typeid", "type": "INTEGER"},
    {"name": "type_name", "type": "STRING"},
    {"name": "phone_number", "type": "STRING"},
    {"name": "start_date", "type": "DATE"},
    {"name": "start_time", "type": "TIME"},
    {"name": "end_date", "type": "DATE"},
    {"name": "end_time", "type": "TIME"},
    {"name": "call_duration", "type": "TIME"},
    {"name": "data_used", "type": "FLOAT64"}
  ]
  EOF
}

resource "google_bigquery_table" "example_external_table" {
  dataset_id = "sharaon_mobile_usage"
  project    = var.project
  table_id   = "mobile_usage_data_ext"
  deletion_protection=false

  external_data_configuration {
    autodetect    = true
    source_format = "NEWLINE_DELIMITED_JSON"
    source_uris   = ["gs://sharaon-stage-data-bucket/current/mobile_usage_data.json"]
  }
}