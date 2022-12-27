import boto3
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table = dynamodb.Table('relaylist')

response = table.scan(FilterExpression=Attr("enabled").eq(True))

print(response)