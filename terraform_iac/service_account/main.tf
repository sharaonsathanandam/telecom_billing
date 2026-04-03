resource "google_service_account" "my_service_account" {
  account_id   = var.account_id
  display_name = var.service_account_name
  project      = var.project
}

resource "google_service_account_key" "my_service_account_key" {
  service_account_id = google_service_account.my_service_account.name
}