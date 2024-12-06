import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Received event: {event}")
    
    detail = event.get("detail", {})
    
    amount = detail.get("amount", 0)
    if amount > 500:
        priority = "high-priority"
    else:
        priority = "low-priority"
    
    detail["priority"] = priority
    event["detail"] = detail
    
    logger.info(f"Enriched event: {event}")
    
    return event
