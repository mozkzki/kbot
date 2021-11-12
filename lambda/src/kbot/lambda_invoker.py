import boto3
import json
from typing import Dict


def invoke(function_name: str, input_event: Dict):
    Payload = json.dumps(input_event)
    print("payload: {}".format(Payload))

    response = boto3.client("lambda").invoke(
        FunctionName=function_name, InvocationType="Event", Payload=Payload
    )
    print("response: {}".format(response))
