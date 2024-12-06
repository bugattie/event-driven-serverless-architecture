import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Received event: {event}")

    detail = event.get('detail', {})

    required_keys = ['category', 'amount', 'customerId']
    missing_keys = [key for key in required_keys if key not in detail]

    if missing_keys:
        error_message = f"Missing required keys in 'detail': {missing_keys}"
        logger.error(error_message)
        raise Exception(json.dumps({
            "error": "ValidationError",
            "cause": error_message
        }))

    if detail['amount'] <= 0:
        error_message = "Invalid amount; must be greater than zero."
        logger.error(error_message)
        raise Exception(json.dumps({
            "error": "ValidationError",
            "cause": error_message
        }))

    if not isinstance(detail['customerId'], str) or not detail['customerId'].startswith("CUST"):
        error_message = "Invalid customerId; must start with 'CUST'."
        logger.error(error_message)
        raise Exception(json.dumps({
            "error": "ValidationError",
            "cause": error_message
        }))

    logger.info("Validation passed for event.")
    return {
        "statusCode": 200,
        "body": json.dumps("Order validated successfully"),
        "detail": detail
    }
