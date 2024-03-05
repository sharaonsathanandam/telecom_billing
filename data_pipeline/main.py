import json
import random
from faker import Faker
from datetime import datetime, timedelta
from google.cloud import storage

fake = Faker()
def generate_phone_call_data():
    phone_number = fake.phone_number()
    start_timestamp = fake.date_time_between(start_date='-30d', end_date='now')
    end_timestamp = start_timestamp + timedelta(minutes=random.randint(1, 60))
    typeid=1000
    return {
        'phone_number': phone_number,
        'start_timestamp': start_timestamp.isoformat(),
        'end_timestamp': end_timestamp.isoformat(),
        'typeid':typeid
    }

def generate_sms_data():
    phone_number = fake.phone_number()
    typeid=1001
    return {
        'phone_number': phone_number,
        'typeid':typeid
    }

def generate_mobile_internet_data():
    start_timestamp = fake.date_time_between(start_date='-30d', end_date='now')
    end_timestamp = start_timestamp + timedelta(minutes=random.randint(1, 60))
    data_used = random.randint(1, 1000) + round(random.uniform(0, 1), 1)
    typeid=1002
    return {
        'start_timestamp': start_timestamp.isoformat(),
        'end_timestamp': end_timestamp.isoformat(),
        'data_used': data_used,
        'typeid':typeid
    }

def upload_to_gcs(bucket_name, data, path):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(path)
    data_bytes = data.encode('utf-8')
    blob.upload_from_string(data_bytes, content_type='application/json')

def batchloader():
    fake_data_list = []
    data_generation_functions = [generate_phone_call_data, generate_sms_data, generate_mobile_internet_data]
    weights = [3, 1, 3]

    for _ in range(100):
        fake_data_list = fake_data_list + [random.choices(data_generation_functions, weights=weights)[0]()]

    # json_data = json.dumps(fake_data_list)
    json_data = '\n'.join(json.dumps(item) for item in fake_data_list)

    bucket_name = 'sharaon-stage-data-bucket'
    upload_to_gcs(bucket_name, json_data, 'current/mobile_usage_data.json')

batchloader()