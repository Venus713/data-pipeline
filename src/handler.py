import re
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
        body = event['body']
        body = body.replace(u'\xa0', u'')

        r_csv = re.search(
            r'Content-Type: text/csv(.*\,[\w]*)',
            body,
            re.DOTALL
        )
        lst = [i for i in r_csv.group(1).split('\n') if (i.find('\r') == -1)]
        file_content = [i.split(',') for i in lst]

        match = re.search(r';\s?filename\=\"(.*)\"', body)
        if match:
            filename = match.groups()[0]
        else:
            filename = ''

        pk = filename.split('.')[0]

        header = file_content[0]
        file_content.pop(0)

        items = []
        for elem in file_content:
            item = {}
            for i in range(len(header)):
                item.update({
                    header[i]: elem[i]
                })
            items.append(item)
        logger.info(f'items: {items}')
        try:
            for item in items:
                sk = item.pop(header[0])
                resp = dynamodb.create_item(pk, sk, item)
                logger.info(
                    f'response in create_item: {json.dumps(resp, indent=2)}')
            return build_response(200, None, 'successfully imported!')
        except Exception as e:
            print(e)
            print('4444444444444444444444')
            logger.debug(f'Exception in create_item: {e.__str__()}')
            return build_response(400, None, e.__str__())
