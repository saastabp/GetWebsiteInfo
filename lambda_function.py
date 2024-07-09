import boto3
import json
import logging
import os
from decimal import Decimal

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # DynamoDB setup
    dynamodb = boto3.resource('dynamodb')
    tbl_name = os.environ['TABLE_NAME']
    table = dynamodb.Table(tbl_name)

    # Scan DynamoDB for news items
    try:
        response = table.scan()  # Scan the table for items
        items = response['Items']

        logger.info(f"Items retrieved: {len(items)}")
    except Exception as e:
        logger.error(f"Error scanning DynamoDB: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps("Error scanning DynamoDB")
        }

    # Return the items
    return {
        'statusCode': 200,
        'body': json.dumps(items, default=decimal_serializer)
    }
    
def decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Type not serializable")
