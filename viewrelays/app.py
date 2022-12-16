import urllib.request
import json 
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table = dynamodb.Table('relaylist')

response = table.scan()

def lambda_handler(event, context):

    data = json.dumps(response['Items'])

    return {
        "statusCode": 200,
        "body": data,
    }
