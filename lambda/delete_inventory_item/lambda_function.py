import json
import boto3
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

def lambda_handler(event, context):
    table = boto3.resource('dynamodb').Table('Inventory')

    item_id = event.get('pathParameters', {}).get('id')
    location_id_raw = event.get('queryStringParameters', {}).get('location_id')

    if not item_id or not location_id_raw:
        return {
            'statusCode': 400,
            'body': json.dumps("Both 'id' and 'location_id' are required.")
        }

    try:
        location_id = int(location_id_raw)
    except ValueError:
        return {
            'statusCode': 400,
            'body': json.dumps("location_id must be a number.")
        }

    try:
        table.delete_item(Key={
            'id': item_id,
            'location_id': location_id
        })
        return {
            'statusCode': 200,
            'body': json.dumps(f"Deleted item {item_id} at location {location_id}.")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting item: {str(e)}")
        }
