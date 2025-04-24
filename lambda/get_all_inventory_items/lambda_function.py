import json
import boto3

def lambda_handler(event, context):
    table = boto3.resource('dynamodb').Table('Inventory')
    try:
        response = table.scan()
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'])
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error retrieving items: {str(e)}")
        }
