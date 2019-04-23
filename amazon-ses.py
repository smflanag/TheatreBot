import boto3
from botocore.exceptions import ClientError
from theatrebot import theatre_bot
from settings import sender_email, recipient_email


SENDER = sender_email
RECIPIENT = recipient_email

AWS_REGION = "eu-west-1"
SUBJECT = "TheatreBot update"
BODY_HTML = theatre_bot()


CHARSET = "UTF-8"
client = boto3.client('ses', region_name=AWS_REGION)


try:
    response = client.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': BODY_HTML,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,
    )

except ClientError as e:
    print(e.response['Error']['Message'])
else:
    print("Email sent! Message ID:"),
    print(response['MessageId'])
