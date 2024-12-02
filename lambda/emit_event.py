import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

eventbridge = boto3.client('events')


def lambda_handler(event, context):
    logger.info(f"Received event: {event}")
    
    try:
        for record in event.get("Records", []):
            body = json.loads(record["body"])
            
            event_entry = {
                "Source": body["Source"],
                "DetailType": body["DetailType"],
                "EventBusName": body["EventBusName"],
                "Detail": json.dumps(body["Detail"])
            }

            logger.info(f"Event to put: {event_entry}")
            
            response = eventbridge.put_events(
                Entries=[event_entry]
            )
            
            logger.info(f"Event emitted successfully: {response}")

        return {
            "statusCode": 200,
            "body": json.dumps("Event sent successfully")
        }
    except Exception as exp:
        logger.exception(exp)
        return {
            "statusCode": 500,
            "body": json.dumps("An unexpected error occurred while emitting the event.")
        }
    
