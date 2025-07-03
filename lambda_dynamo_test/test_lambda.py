import json
import boto3
from moto import mock_dynamodb2
from lambda_function import lambda_handler

@mock_dynamodb2
def test_lambda_handler():
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.create_table(
        TableName='userTable',
        KeySchema=[{'AttributeName': 'userID', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'userID', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )
    table.wait_until_exists()

    event = {
        'body': json.dumps({
            'userID': '123',
            'name': 'Alice',
            'email': 'alice@example.com'
        })
    }

    response = lambda_handler(event, None)
    body = json.loads(response['body'])

    assert response['statusCode'] == 200
    assert body['message'] == 'User saved successfully!'

    result = table.get_item(Key={'userID': '123'})
    assert 'Item' in result
    assert result['Item']['name'] == 'Alice'
    assert result['Item']['email'] == 'alice@example.com'
