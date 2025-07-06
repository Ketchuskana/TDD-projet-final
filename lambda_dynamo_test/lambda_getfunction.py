import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    print("Received event:", event)
    params = event.get('queryStringParameters') or {}
    user_id = params.get('userID')

    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table('userTable-dev') 

    try:
        params = event.get('queryStringParameters') or {}
        user_id = params.get('userID')
        # user_id = event['queryStringParameters']['userID']
    except (TypeError, KeyError):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing userID in query parameters'})
        }

    try:
        response = table.get_item(Key={'userID': user_id})
        if 'Item' in response:
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item'])
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'User not found'})
            }
    except ClientError as e:
        print("ClientError:", e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Could not retrieve user'})
        }
