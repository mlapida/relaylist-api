import urllib.request
import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table = dynamodb.Table('relaylist')

response = table.scan()
data = response['Items']

# print(data)

hdr = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

for relay in data:

    try:
        data = json.load(urllib.request.urlopen(
            urllib.request.Request(relay['url'], headers=hdr)))
    except:
        print('Issue with site')

    try:
        if data['version'] == '2.0':
            output = relay['name'] + " (Open: " + str(data['openRegistrations']) + \
                "): " + str(len(data['metadata']['peers']))
            
            table.put_item(
                Item={
                    'name': relay['name'],
                    'url' : relay['url'],
                    'open': bool(data['openRegistrations']),
                    'server_count': str(len(data['metadata']['peers'])),
                }
            )

        elif data['version'] == '2.1':
            output = relay['name'] + " (Open: " + str(data['openRegistrations']) + "): " + \
            str(data['usage']['users']['activeMonth'])

            table.put_item(
                Item={
                    'name': relay['name'],
                    'url' : relay['url'],
                    'open': bool(data['openRegistrations']),
                    'server_count': str(len(data['metadata']['peers'])),
                }
            )

        print(output)
    except:
        print('Issue with data')
