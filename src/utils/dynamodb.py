import boto3
import os
import logging
from typing import Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DynamoDB:
    table_name = os.environ['DB_TABLE_NAME']

    def __init__(self):
        if not self.table_name:
            raise ValueError('table_name property can not be empty.')

        dynamo_db = boto3.resource(
            'dynamodb', region_name=os.environ['REGION'])

        self.__table = dynamo_db.Table(self.table_name)

    def create_item(self, pk: str, sk: Any, item: dict):
        '''
        save new item into dynamodb table
        '''
        item.update({
            'pk': pk,
            'sk': sk
        })
        return self.__table.put_item(Item=item)

    def get_item(self, pk: str, sk: Any) -> dict:
        """
        get a item from dynamodb table
        """
        item = self.__table.get_item(Key={'pk': pk, 'sk': sk})
        return item.get('Item', {})
