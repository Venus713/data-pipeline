import json

import boto3

from .utils.dynamodb import DynamoDB, logger
from .utils.responses import build_response

s3_client = boto3.client('s3')
dynamodb = DynamoDB()


def import_csv_to_db(event, context):
    logger.info(
        f'Received event: {json.dumps(event, indent=2)}')
    if event:
        return build_response(200, None, 'successfully imported!')
