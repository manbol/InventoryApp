import json
import boto3
import ulid
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

def lambda_handler(event, context):
    try:
        data = json.loads(event['body'])
    except (KeyError, json.JSONDecodeError):
        return {
            'statusCode': 400,
            'body': json.dumps("Invalid request body.")
        }

    item_id = str(ulid.new())

    try:
        table = boto3.resource('dynamodb').Table('Inventory')
        table.put_item(Item={
            'id': item_id,
            'name': data['name'],
            'description': data['description'],
            'qty': int(data['qty']),
            'price': Decimal(str(data['price'])),  # ✅ Fixed
            'location_id': int(data['location_id'])
        })

        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {item_id} added successfully.")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error adding item: {str(e)}")
        }
