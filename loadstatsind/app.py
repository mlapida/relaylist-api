import urllib.request
import json
import boto3
import time
from cerberus import Validator

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table = dynamodb.Table('relaylist')


def lambda_handler(event, context):
    print(event)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15'}

    try:

        getURL = json.load(urllib.request.urlopen(
            urllib.request.Request(event['url']+".well-known/nodeinfo", headers=hdr)))

        data = json.load(urllib.request.urlopen(
            urllib.request.Request(getURL['links'][0]['href'], headers=hdr)))

        try:
            if data['version'] == '2.0':
                output = event['name'] + " (Open: " + str(data['openRegistrations']) + \
                    "): " + str(len(data['metadata']['peers']))

                updateTable(event['name'], bool(data['openRegistrations']), str(
                    len(data['metadata']['peers'])))

            elif data['version'] == '2.1':

                output = event['name'] + " (Open: " + str(data['openRegistrations']) + "): " + \
                    str(data['usage']['users']['activeMonth'])

                updateTable(event['name'], bool(data['openRegistrations']), str(
                    data['usage']['users']['activeMonth']))

            print(output)
        except Exception as e:
            print('Issue with data: ' + str(e))

    except Exception as e:

        t = time.time()

        table.update_item(
            Key={
                'name': event['name']
            },
            UpdateExpression='SET up = :up, updated = :updated',
            ExpressionAttributeValues={
                ':up': False,
                ':updated': str(int(t))
            }
        )

        print('Issue with site: ' + event['name'] + " " + str(e))

    return


def updateTable(name, reg, server_count):

    t = time.time()

    v = Validator()

    v.schema = {'reg': {'type': 'boolean'}, 'servercount': {'type': 'string', 'minlength': 1, 'maxlength': 5}}

    document = {'reg': reg, 'servercount': server_count}

    if v.validate(document) is True:

        table.update_item(
            Key={
                'name': name
            },
            UpdateExpression='SET openRegistrations = :openRegistrations, server_count = :server_count, up = :up, updated = :updated',
            ExpressionAttributeValues={
                ':up': True,
                ':openRegistrations': reg,
                ':server_count': server_count,
                ':updated': str(int(t))
            }
        )
    else:
        print("Issue with validation of data")
