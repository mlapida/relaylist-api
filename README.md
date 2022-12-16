# Relaylist API

This is the API for [RelayList.com](https://relaylist.com).

API Endpoint: [api.relaylist.com](https://api.relaylist.com)

There are three primary components:

1. Storage - A DynamoDB table for tracking relays.
2. Updater - A Lambda function run on a cron to update the participating servers in the relay.
3. API - A Lambda function and API Gateway to query the relays.

## Todo
- [ ] Add additional information fields in DynamoDB
- [ ] Track users on participating servers to guage actual volume 
- [ ] Update tests