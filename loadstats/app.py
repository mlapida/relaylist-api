import urllib.request
import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table = dynamodb.Table('relaylist')

response = table.scan()

def lambda_handler(event, context):

    data = response['Items']

    hdr = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    
    for relay in data:

        try:
            info = json.load(urllib.request.urlopen(
                urllib.request.Request(relay['url'], headers=hdr)))
        except:
            print('Issue with site')

        try:
            if info['version'] == '2.0':
                output = relay['name'] + " (Open: " + str(info['openRegistrations']) + \
                    "): " + str(len(info['metadata']['peers']))
                
                table.put_item(
                    Item={
                        'name': relay['name'],
                        'url' : relay['url'],
                        'open': bool(info['openRegistrations']),
                        'server_count': str(len(info['metadata']['peers'])),
                    }
                )

            elif info['version'] == '2.1':
       
                output = relay['name'] + " (Open: " + str(info['openRegistrations']) + "): " + \
                    str(info['usage']['users']['activeMonth'])

                table.put_item(
                    Item={
                        'name': relay['name'],
                        'url' : relay['url'],
                        'open': bool(info['openRegistrations']),
                        'server_count': str(info['usage']['users']['activeMonth']),
                    }
                )

            print(output)
        except:
            print('Issue with data')


    return 
