import urllib.request
import json 
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table = dynamodb.Table('relaylist')

response = table.scan(FilterExpression=Attr("enabled").eq(True))

data = json.dumps(response['Items'])

def lambda_handler(event, context):

    return {
        "statusCode": 200,
        'headers': {
            #'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET'
        },
        "body": data,
    }