# telecom_billing
A data pipeline with GCP, Python, Pub/Sub, Dataflow, Big Query, Apache Beam, Airflow, Terraform and much more!

## Description:
This project processes sample telecom data and generates a billing report. The sample input data is loaded as both streaming data and batch data. A python program using faker library is used to generate sample data. One program runs on Cloud Function and generates a sample file for batch-loading data into BigQuery. Another program generates streaming data and simulates real-time data streaming. This data is put on Pub/Sub topic and is transformed and loaded into BigQuery table.

## Tools & Technologies used:
* Cloud - Google Cloud Platform
* Infrastructure as Code - Terraform
* Orchestration - Cloud Composer
* Transformation - Dataflow, Cloud Function
* Data Lake - Cloud Storage
* Data Warehouse - BigQuery
* Languages - Python
