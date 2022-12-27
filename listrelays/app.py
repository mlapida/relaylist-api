import urllib.request
import json
import boto3
import time

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
client = boto3.client('lambda')

client = boto3.client('lambda')

table = dynamodb.Table('relaylist')


def lambda_handler(event, context):
    
    response = table.scan()

    data = response['Items']

    for relay in data:

        response = client.invoke(
            FunctionName='arn:aws:lambda:us-west-2:931517136044:function:relaylist-api-LoadStatsFunctionInd-XaUJNY3DiC1v',
            InvocationType='Event', 
            Payload=json.dumps(relay),
        )