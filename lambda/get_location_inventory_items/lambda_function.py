import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    table = boto3.resource('dynamodb').Table('Inventory')
    location_id = event.get('pathParameters', {}).get('id')

    if not location_id:
        return {
            'statusCode': 400,
            'body': json.dumps("Location ID is required.")
        }

    try:
        response = table.query(
            IndexName='location_index',
            KeyConditionExpression=Key('location_id').eq(int(location_id))
        )
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'])
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error querying items: {str(e)}")
        }
