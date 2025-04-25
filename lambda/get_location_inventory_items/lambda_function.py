import json
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

def lambda_handler(event, context):
    location_id_raw = event.get('pathParameters', {}).get('id')

    if not location_id_raw:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'location_id' in path parameters.")
        }

    try:
        location_id = int(location_id_raw)
    except ValueError:
        return {
            'statusCode': 400,
            'body': json.dumps("location_id must be a number.")
        }

    try:
        table = boto3.resource('dynamodb').Table('Inventory')
        response = table.query(
            IndexName='location_index',
            KeyConditionExpression=Key('location_id').eq(location_id)
        )
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'], cls=DecimalEncoder)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error querying items: {str(e)}")
        }
