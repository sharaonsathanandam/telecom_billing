variable "project" {
  description = "The Google Cloud project ID."
}

variable "name" {
  description = "The name of the cloud function to be deployed."
}

variable "desc" {
  description = "The description of the cloud function to be deployed."
}

variable "src_arch_bkt" {
  description = "The cloud storage bucket location where source program is."
}

variable "src_arch_obj" {
  description = "The cloud storage object location where source program is."
}

variable "ent_pt" {
  description = "The entry point name of the program to be executed."
}