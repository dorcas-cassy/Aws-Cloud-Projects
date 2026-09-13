import json
import os

import boto3


sns = boto3.client("sns")
TOPIC_ARN = os.environ["TOPIC_ARN"]


def lambda_handler(event, context):
    try:
        body = event.get("body", event)

        if isinstance(body, str):
            body = json.loads(body)

        subject = body.get("subject", "Event Announcement")
        message = body.get("message")

        if not message:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "error": "The message field is required."
                })
            }

        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject=subject[:100],
            Message=message
        )

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "Announcement sent successfully."
            })
        }

    except (json.JSONDecodeError, AttributeError):
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": "Invalid request body."
            })
        }

    except Exception as error:
        print(f"Error: {error}")

        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": "The announcement could not be sent."
            })
        }
