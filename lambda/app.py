import json
import boto3
import os
import logging
import uuid
from decimal import Decimal
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
table_name = os.getenv("TABLE_NAME")

def extract_event_entry(detail):
    return {
        "orderId": str(uuid.uuid4()),
        "category": detail["category"],
        "amount": Decimal(detail["amount"]),
        "customerId": detail["customerId"]
    }

def lambda_handler(event, context):
    try:
        logger.info(f"Received Event: {event}")
        
        event_body = {}
        
        for record in event.get("Records", []):
            if record.get("eventSource") == "aws:sqs":
                event_body = json.loads(record["body"])["detail"]
            
            elif record.get("EventSource") == "aws:sns":
                sns_message = json.loads(record["Sns"]["Message"])
                event_body = sns_message["detail"]

            event_entry = extract_event_entry(event_body)
            logger.info(f"Item to put: {event_entry}")
            
            table = dynamodb.Table(table_name)
            table.put_item(Item=event_entry)

            logger.info(f"Order added to DynamoDB: {event_entry}")
        
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Order processed successfully!"})
        }
    except ClientError as e:
        logger.error(f"DynamoDB ClientError: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error writing to DynamoDB", "error": str(e)})
        }
    except Exception as exp:
        logger.exception(exp)
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error processing order", "error": str(exp)})
        }

