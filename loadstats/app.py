import urllib.request
import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table = dynamodb.Table('relaylist')

response = table.scan()

def lambda_handler(event, context):

    data = response['Items']

    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15'}
    
    for relay in data:

        try:
            data = json.load(urllib.request.urlopen(
                urllib.request.Request(relay['nodeinfo_url'], headers=hdr)))

            up = True    

        except Exception as e:
            
            up = False

            print('Issue with site: ' + relay['nodeinfo_url'] + " " + str(e))

        try:
            if data['version'] == '2.0':
                output = relay['name'] + " (Open: " + str(data['openRegistrations']) + \
                    "): " + str(len(data['metadata']['peers']))
                
                table.put_item(
                    Item={
                        'name': relay['name'],
                        'url' : relay['url'],
                        'nodeinfo_url' : relay['nodeinfo_url'],
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
                        'nodeinfo_url' : relay['nodeinfo_url'],
                        'open': bool(data['openRegistrations']),
                        'server_count': str(data['usage']['users']['activeMonth']),
                    }
                )

            print(output)
        except Exception as e:
            print('Issue with data: ' + str(e))


    return 
