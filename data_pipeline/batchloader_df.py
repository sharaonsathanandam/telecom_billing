import apache_beam as beam
import json
from datetime import datetime
from apache_beam.io import ReadFromText, WriteToBigQuery
from apache_beam.options.pipeline_options import PipelineOptions
import logging

class TransformData(beam.DoFn):
    def process(self, element):

        out_rec = {}
        record = json.loads(element)

        type_mapping = {
            1000: 'phone_call',
            1001: 'sms',
            1002: 'mobile_internet'
        }

        out_rec['type_name'] = type_mapping.get(record.get('typeid', ''), '')

        start_timestamp_str = record.get('start_timestamp', '')
        if start_timestamp_str:
            start_timestamp_obj = datetime.strptime(start_timestamp_str, '%Y-%m-%dT%H:%M:%S')
            out_rec['start_date'] = start_timestamp_obj.strftime('%Y-%m-%d')
            out_rec['start_time'] = start_timestamp_obj.strftime('%H:%M:%S')

        end_timestamp_str = record.get('end_timestamp', '')
        if end_timestamp_str:
            end_timestamp_obj = datetime.strptime(end_timestamp_str, '%Y-%m-%dT%H:%M:%S')
            out_rec['end_date'] = end_timestamp_obj.strftime('%Y-%m-%d')
            out_rec['end_time'] = end_timestamp_obj.strftime('%H:%M:%S')

        if start_timestamp_str and end_timestamp_str:
            time_difference = end_timestamp_obj - start_timestamp_obj
            seconds = int(time_difference.total_seconds())
            hours, remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            out_rec['call_duration'] = f"{hours:02}:{minutes:02}:{seconds:02}"

        out_rec['typeid'] = record.get('typeid')
        out_rec['phone_number'] = record.get('phone_number','')
        out_rec['data_used'] = record.get('data_used','')

        return [out_rec]

class MoveToArchiveFolder(beam.DoFn):
    def process(self, element):
        import subprocess
        archive_file_name = f"mobile_usage_data.json_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        archive_file_path = f"gs://sharaon-stage-data-bucket/archive/{archive_file_name}"
        move_command = f"gsutil mv gs://sharaon-stage-data-bucket/current/mobile_usage_data.json {archive_file_path}"
        subprocess.run(move_command, shell=True)
        yield element

def run():
    logging.getLogger().setLevel(logging.DEBUG)

    input_gcs_path = 'gs://sharaon-stage-data-bucket/current/mobile_usage_data.json'
    options = PipelineOptions()

    with (beam.Pipeline(options=options) as p):
        lines = p | 'ReadFromGCS' >> ReadFromText(input_gcs_path)
        lines | 'TransformData' >> beam.ParDo(TransformData())  \
              | 'WriteToBigQuery' >> WriteToBigQuery(
              table='sunny-might-415700.sharaon_mobile_usage.mobile_usage_data',
              schema='typeid:INTEGER,type_name:STRING,phone_number:STRING,start_date:DATE,start_time:TIME,end_date:DATE,end_time:TIME,call_duration:TIME,data_used:FLOAT',
              write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
              create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
              custom_gcs_temp_location='gs://sharaon-logs-bucket/staging'), \
            # | 'MoveToArchiveFolder' >> beam.ParDo(MoveToArchiveFolder())

    log_file_path = 'gs://sharaon-stage-data-bucket/logs/dataflow_log.txt'
    upload_command = f"gsutil cp /tmp/dataflow_stdout.log /tmp/dataflow_stderr.log {log_file_path}"
    import subprocess
    subprocess.run(upload_command, shell=True)

if __name__ == '__main__':
    run()