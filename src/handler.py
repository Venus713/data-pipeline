import json
import csv

import boto3

from .utils.dynamodb import DynamoDB, logger
from .utils.responses import build_response

s3_client = boto3.client('s3')
dynamodb = DynamoDB()


def import_csv_to_db(event, context):
    logger.info(
        f'Received event: {json.dumps(event, indent=2)}')
    if event:
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        file_key = event['Records'][0]['s3']['object']['key']

        logger.info(f'Reading {file_key}, {bucket_name}')

        pk = file_key.split('.')[0]

        csvfile = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        csvcontent = csvfile['Body'].read().decode('utf-8').splitlines()
        data = csv.DictReader(csvcontent)

        try:
            for item in data:
                sk = next(iter(item.values()))
                resp = dynamodb.create_item(pk, sk, item)
                logger.info(
                    f'response in create_item: {json.dumps(resp, indent=2)}')
            return build_response(200, None, 'successfully imported!')
        except Exception as e:
            logger.debug(f'Exception in create_item: {e.__str__()}')
            return build_response(400, None, e.__str__())
