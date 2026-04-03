output "service_account_key_file" {
  value = google_service_account_key.my_service_account_key.private_key
}