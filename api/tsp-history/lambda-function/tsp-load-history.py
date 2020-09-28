import json
import boto3

dynamodb_tsp_history_tbl = boto3.resource('dynamodb').Table('tsp-history')

def lambda_handler(event, context):
    try:
        hist_list = dynamodb_tsp_history_tbl.scan()["Items"]
        contents_dict = {}
        for i, hist in enumerate(hist_list):
            hist["name"] = hist["csv_url"].split('_')[-1].split('.')[0]
            contents_dict[str(i+1)] = hist
        code = 200
        contents = json.dumps(contents_dict)
    except Exception as e:
        print(e)
        code = 500
        contents = json.dumps({
            "error_message": str(e),
        })
    return {
        'statusCode': code,
        'body': contents,
        'isBase64Encoded': False,
        'headers': {"Content-Type": "application/json"}
    }
