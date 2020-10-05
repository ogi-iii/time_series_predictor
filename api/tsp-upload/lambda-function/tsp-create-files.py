import json
import boto3
import datetime
import base64

img_s3 = boto3.resource('s3')
csv_s3 = boto3.resource('s3')
dynamodb_tsp_history_tbl = boto3.resource('dynamodb').Table('tsp-history')
sts = boto3.client('sts').get_caller_identity()

def lambda_handler(event, context):
    aws_id = str(sts['Account'])
    img_bucket = 'tsp-img-' + aws_id
    csv_bucket = 'tsp-csv-' + aws_id
    date_time = str(datetime.datetime.now())
    try:
        body = json.loads(event.get("body"))
        img_url = _output_files(img_s3, img_bucket, body, "img_base64", "png", date_time)
        csv_url = _output_files(csv_s3, csv_bucket, body, "csv_str", "csv", date_time)
        dynamodb_tsp_history_tbl.put_item(
            Item = {
                "timestamp": date_time,
                "img_url": img_url,
                "csv_url": csv_url,
            }
        )
        code = 200
        contents = json.dumps({
            "img_url": img_url,
            "csv_url": csv_url,
        })
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

def _output_files(s3, bct_name, body, b_content, type_str, date_time):
    f_name = body['fname'].split('/')[-1].split('.')[0]
    key = f'{date_time}_{f_name}.{type_str}'
    url = f"https://{bct_name}.s3-ap-northeast-1.amazonaws.com/{key.replace(' ', '+').replace(':', '%3A')}"
    obj = s3.Object(bct_name, key)
    if type_str == 'png' or type_str == 'jpg':
        contents = base64.b64decode(body[b_content].encode('utf-8'))
    else:
        contents = body[b_content]
    obj.put(ACL='public-read', Body=contents)
    return url
