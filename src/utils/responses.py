import json

from typing import Any


def build_response(status_code: Any, body: Any, msg: str) -> dict:
    return {
        'statusCode': status_code,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*"
        },
        'body': json.dumps({
            'data': body,
            'message': msg
        })
    }
