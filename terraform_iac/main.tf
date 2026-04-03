provider "google" {
  alias       = "main"
  config      = file("./providers.tf")
}

module "service_account" {
  source               = "./service_account"
  account_id           = var.account_id
  service_account_name = var.sa_name
  project              = var.project_id
}

module "cloud_storage" {
  source      = "./gcs"
  project     = var.project_id
}

module "cloud_function" {
  source      = "./cloud_function"
  project     = var.project_id
}

module "big_query" {
  source      = "./big_query"
  project     = var.project_id
}