import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import StandardOptions

class TransformData(beam.DoFn):
    def process(self, element):

        out_rec = {}
        record = json.loads(element)

        type_mapping = {
            1000: 'phone_call',
            1001: 'sms',
            1002: 'mobile_internet'
        }

        record['type_name'] = type_mapping.get(record.get('typeid', ''), '')

        start_timestamp_str = record.get('start_timestamp', '')
        if start_timestamp_str:
            start_timestamp_obj = datetime.strptime(start_timestamp_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            out_rec['start_date'] = start_timestamp_obj.strftime('%Y-%m-%d')
            out_rec['start_time'] = start_timestamp_obj.strftime('%H:%M:%S')

        end_timestamp_str = record.get('end_timestamp', '')
        if end_timestamp_str:
            end_timestamp_obj = datetime.strptime(end_timestamp_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            out_rec['end_date'] = end_timestamp_obj.strftime('%Y-%m-%d')
            out_rec['end_time'] = end_timestamp_obj.strftime('%H:%M:%S')

        if start_timestamp_str and end_timestamp_str:
            out_rec['call_duration'] = end_timestamp_obj - start_timestamp_obj

        out_rec['typeid'] = record.get('typeid')
        out_rec['phone_number'] = record.get('phone_number','')
        out_rec['data_used'] = record.get('data_used','')

        return [out_rec]

class PubsubToBigQueryOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument('--project', help='Google Cloud Project ID')
        parser.add_argument('--input_topic', help='Input Pub/Sub topic')
        parser.add_argument('--output_table', help='Output BigQuery table')


def run():
    options = PipelineOptions()
    options.view_as(StandardOptions).runner = 'DataflowRunner'
    pubsub_bq_options = options.view_as(PubsubToBigQueryOptions)
    pubsub_bq_options.project = 'your-gcp-project-id'
    pubsub_bq_options.input_topic = 'projects/your-gcp-project-id/topics/your-input-topic'
    pubsub_bq_options.output_table = 'your-gcp-project-id:your-dataset.your-table'

    with beam.Pipeline(options=options) as pipeline:
        pubsub_data = (pipeline
                       | 'Read from Pub/Sub' >> beam.io.ReadFromPubSub(subscription=pubsub_bq_options.input_topic)
                       | 'TransformData' >> beam.ParDo(TransformData())
                       )

        pubsub_data | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
            table=pubsub_bq_options.output_table,
            schema='your_schema',  # Replace with your BigQuery schema
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
        )

if __name__ == '__main__':
    run()
