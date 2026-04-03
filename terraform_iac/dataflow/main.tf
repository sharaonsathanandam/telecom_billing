resource "google_dataflow_job" "example_job" {
  name     = "telecomm-dataflow-job"
  project  = var.project
  region   = "us-central1"

  template_gcs_path = "gs://dataflow-templates/latest/GCS_Text_to_BigQuery"
  temp_gcs_location = "gs://sharaon-logs-bucket/temp"

  parameters = {
    inputFilePattern  = "gs://sharaon-stage-data-bucket/current/mobile_usage_data.json"
    JSONPath          = "gs://sharaon-code-bucket/schema.json"
    outputTable       = "sunny-might-415700.sharaon_mobile_usage.mobile_usage_data"
    bigQueryLoadingTemporaryDirectory = "gs://sharaon-logs-bucket/temp"
  }
  additional_experiments = ["worker_region=us-central1", "stagingLocation=gs://sharaon-logs-bucket/temp", "--pyfiles=gs://sharaon-code-bucket/batchloader_df.py"]
  on_delete = "cancel"
}
