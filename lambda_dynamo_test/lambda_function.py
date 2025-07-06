import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    print("Received event:", event)
    print("EVENT:", json.dumps(event))

    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table('userTable-dev')

    try:
        if 'body' in event:
            data = json.loads(event['body'])
        else:
            data = event

        user_id = data['userID']
        name = data['name']
        email = data['email']

        table.put_item(
            Item={
                'userID': user_id,
                'name': name,
                'email': email
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User saved successfully!'})
        }
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'Missing field {str(e)}'})
        }
    except ClientError as e:
        print("ClientError:", e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Could not save user'})
        }
