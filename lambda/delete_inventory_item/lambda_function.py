import json
import boto3

def lambda_handler(event, context):
    table = boto3.resource('dynamodb').Table('Inventory')
    item_id = event.get('pathParameters', {}).get('id')

    if not item_id:
        return {
            'statusCode': 400,
            'body': json.dumps("Item ID is required.")
        }

    try:
        table.delete_item(Key={'id': item_id})
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item {item_id} deleted.")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting item: {str(e)}")
        }
