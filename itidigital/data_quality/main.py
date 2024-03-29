import boto3
from moto import mock_sqs

import itidigital.data_quality.event_validator as event_validator


@mock_sqs
def main(raw_event: dict):
    _SQS_CLIENT = boto3.client('sqs', region_name='us-east-1')
    _SQS_CLIENT.create_queue(
        QueueName='valid-events-queue'
    )
    event_validator._SQS_CLIENT = _SQS_CLIENT
    event_validator.handler(raw_event)


if __name__ == "__main__":
    event = {
        "eid": "3e628a05-7a4a-4bf3-8770-084c11601a12",
        "documentNumber": "42323235600",
        "name": "Joseph",
        "age": 32,
        "address": {
            "street": "St. Blue",
            "number": 3,
            "mailAddress": True
        }
    }

    main(raw_event=event)
