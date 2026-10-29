import json
import urllib.parse
import boto3

print('Loading function')

# Initialize both service clients
s3 = boto3.client('s3')
sns = boto3.client('sns')

# CRITICAL: Replace this with your actual SNS Topic ARN from the AWS Console
SNS_TOPIC_ARN = 'arn:aws:sns:your-region:123456789012:your-topic-name'

def lambda_handler(event, context):
    # Get the object details from the S3 trigger event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    # Extract just the file name from the path for the clean message string
    text_file_name = key.split('/')[-1]
    
    try:
        # 1. Fetch the text file from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        
        # 2. Read the body content and decode it into a standard string
        file_content = response['Body'].read().decode('utf-8')
        
        # 3. Calculate the word count by splitting the string on whitespace
        word_count = len(file_content.split())
        
        # 4. Format the custom message string exactly as requested
        message_body = f"The word count in the {text_file_name} file is {word_count}."
        
        # 5. Publish the notification to the SNS Topic
        sns_response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f"Word Count Results: {text_file_name}",
            Message=message_body
        )
        
        print(f"Successfully processed {text_file_name}. Sent SNS message ID: {sns_response['MessageId']}")
        return message_body

    except Exception as e:
        print(e)
        print(f"Error processing object {key} from bucket {bucket}.")
        raise e
