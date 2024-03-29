import os
import json
import boto3

from itidigital import variables
from itidigital.utils.schema import helpers
from itidigital.utils.schema.builder import SchemaBuilder
from itidigital.data_quality.event.builder import EventBuilder
from itidigital.data_quality.event.validator import EventValidator

_SQS_CLIENT = None
_VALID_EVENTS_QUEUE_NAME = 'valid-events-queue'
_SCHEMA_FILE_PATH = os.path.join(
        variables.PROJECT_ROOT_PATH,
        'itidigital/data_quality/schema.json'
)



def send_event_to_queue(event, queue_name):
    """
     Responsável pelo envio do evento para uma fila
    :param event: Evento  (dict)
    :param queue_name: Nome da fila (str)
    :return: None
    """
    
    sqs_client = boto3.client("sqs", region_name="us-east-1")
    response = sqs_client.get_queue_url(
        QueueName=queue_name
    )
    queue_url = response['QueueUrl']
    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(event)
    )
    print(f"Response status code: [{response['ResponseMetadata']['HTTPStatusCode']}]")


def handler(raw_event):
    """
    #  Função principal que é sensibilizada para cada evento
    Aqui você deve começar a implementar o seu código
    Você pode criar funções/classes à vontade
    Utilize a função send_event_to_queue para envio do evento para a fila,
        não é necessário alterá-la
    """
    raw_schema = helpers.load_schema(file_path=_SCHEMA_FILE_PATH)

    event = EventBuilder(config=raw_event).construct()
    schema = SchemaBuilder(config=raw_schema).construct()
    validator = EventValidator(schema=schema)

    is_valid_event = validator.is_valid(event=event)

    if is_valid_event:
        send_event_to_queue(
            event=raw_event,
            queue_name=_VALID_EVENTS_QUEUE_NAME
        )
