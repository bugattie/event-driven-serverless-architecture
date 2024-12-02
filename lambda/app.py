import json
import boto3
import os
import logging
import uuid
from decimal import Decimal
from botocore.exceptions import ClientError

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB resource
dynamodb = boto3.resource("dynamodb")
table_name = os.getenv("TABLE_NAME")

def extract_order_details(event_body):
    """
    Extract order details from the parsed event body.
    """
    logger.info(f"Received event_body: {event_body}")

    return {
        "orderId": str(uuid.uuid4()),
        "category": event_body["detail"]["category"],
        "amount": Decimal(event_body["detail"]["amount"]),
        "customerId": event_body["detail"]["customerId"]
    }


def lambda_handler(event, context):
    try:
        logger.info(f"Received Event: {event}")
        
        # Determine the source of the event and parse accordingly
        event_body = None

        # Handle API Gateway invocation
    #     if "httpMethod" in event and event["httpMethod"] == "POST":
    #         logger.info("Event received via API Gateway")
    #         if isinstance(event["body"], str):
    #             event_body = json.loads(event["body"])
    #         else:
    #             event_body = event["body"]
    #     elif "Records" in event and event["Records"][0]["EventSource"] == "aws:sns":
    #         logger.info("Event received via SNS")
    #         sns_message = event["Records"][0]["Sns"]["Message"]
    #         event_body = json.loads(sns_message) if isinstance(sns_message, str) else sns_message
    #     else:
    #         logger.error("Unsupported event format")
    #         raise ValueError("Unsupported event format")

    #      # Handle nested parsing
    #     if "body" in event_body:
    #         inner_body = event_body["body"]
    #         if isinstance(inner_body, str):
    #             inner_body = json.loads(inner_body)
    #         event_body = inner_body
        
    #     # Extract order details
    #     order_details = extract_order_details(event_body)
    #     logger.info(f"Item to put: {order_details}")

    #     # Insert into DynamoDB
    #     table = dynamodb.Table(table_name)
    #     table.put_item(Item=order_details)
    #     logger.info(f"Order added to DynamoDB: {order_details}")
        
    #     # Return success response
    #     return {
    #         "statusCode": 200,
    #         "body": json.dumps({"message": "Order processed successfully!"})
    #     }
    # except ClientError as e:
    #     logger.error(f"DynamoDB ClientError: {e}")
    #     return {
    #         "statusCode": 500,
    #         "body": json.dumps({"message": "Error writing to DynamoDB", "error": str(e)})
    #     }
    except Exception as exp:
        logger.exception(exp)
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error processing order", "error": str(exp)})
        }

