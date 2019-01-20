from __future__ import print_function

import boto3
import json
import urllib2

print('Loading function')
dynamo = boto3.client('dynamodb')
s3 = boto3.resource('s3')

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''
    print("Received event: " + json.dumps(event, indent=2))
    print("Received event: " + str(event))
    object = s3.Object('doramessages', 'messages.txt')
    
    msg = " Message from " + (event['From'])  +  " : " + urllib2.unquote(event['Body'])
    msg = msg.replace("+", " ")
    msg = msg.replace("%2B", "")
    object.put(Body=msg)
    bucket = s3.Bucket('doramessages')
    bucket.Acl().put(ACL='public-read')
    object.Acl().put(ACL='public-read')
    
    return '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'\
               '<Response><Message>Hello world! -Lambda' + msg +'</Message></Response>'
    # else: 
    #     return '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'\
    #           '<Response><Message> Image recieved </Message></Response>'
           
    # operations = {
    #     'DELETE': lambda dynamo, x: dynamo.delete_item(**x),
    #     'GET': lambda dynamo, x: dynamo.scan(**x),
    #     'POST': lambda dynamo, x: dynamo.put_item(**x),
    #     'PUT': lambda dynamo, x: dynamo.update_item(**x),
    # }

    # operation = event['httpMethod']
    # if operation in operations:
    #     payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
    #     return respond(None, operations[operation](dynamo, payload))
    # else:
    #     return respond(ValueError('Unsupported method "{}"'.format(operation)))

