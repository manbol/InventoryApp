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
        response = table.get_item(Key={'id': item_id})
        item = response.get('Item')
        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps("Item not found.")
            }
        return {
            'statusCode': 200,
            'body': json.dumps(item)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error retrieving item: {str(e)}")
        }
