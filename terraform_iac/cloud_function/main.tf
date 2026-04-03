resource "google_cloudfunctions_function" "function" {
  name        = var.name
  description = var.desc
  runtime     = "python312"
  project     = var.project
  source_archive_bucket = var.src_arch_bkt
  source_archive_object = var.src_arch_obj
  trigger_http          = true
  entry_point           = var.ent_pt
}