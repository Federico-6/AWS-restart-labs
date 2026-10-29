# Project Title and Summary
## Title: Event-Driven Word Counter: Automating Text File Analysis with Amazon S3, AWS Lambda, and Amazon SNS
## Project Summary
	- This project builds a serverless, event-driven workflow on AWS. When a `.txt` file is uploaded to an Amazon S3 bucket, an AWS Lambda function runs automatically, counts the words in the file, and publishes the result to an Amazon SNS topic. SNS then emails the count to a subscribed administrator, with the file name in the subject line. The S3 trigger is filtered to the `.txt` suffix, so other file types (such as `.jpg` images) do not invoke the function. No servers are provisioned or managed at any point.
## Tech/Skill Used
### AWS Services
	- AWS Lambda: serverless compute for the word-count logic
	- Amazon S3: object storage and event source
	- Amazon SNS: topic and email subscription for notifications
	- AWS IAM: execution role with permissions for Lambda, S3, SNS, and CloudWatch
	- Amazon CloudWatch: function logging and monitoring
# Problem Statement and Objectives
## Problem Statement
	- Teams that receive text files regularly, such as logs, documents, and submissions, often need quick information about them, like their length. Checking each file by hand is repetitive and doesn’t scale, and running a dedicated server to watch for uploads is costly and adds maintenance overhead for such a small task. This project solves the problem with a serverless pipeline that reacts to each text file upload, computes the word count automatically, and notifies an administrator by email, paying only for the compute used per upload.
## Objectives
	- Create a Lambda function to count the number of words in a text file.
	- Configure an Amazon Simple Storage Service (Amazon S3) bucket to invoke a Lambda function when a text file is uploaded to the S3 bucket.
	- Create an Amazon Simple Notification Service (Amazon SNS) topic to report the word count in an email.
# Architecture Diagram

![unknown_asset](<architecture-diagram/architecture-diagram.png>)

1. User **uploads** a file inside the S3 bucket.
2. If it is a **.txt file** it will trigger the **word-counter** Lambda function.
3. Once triggered, it fetches the file uploaded and counts the number of words inside the file.
4. The output (number of words) is pushed to the **SNS topic (word-count-topic)**.
5. The **SNS topic** broadcasts the information to its subscribers via **email notification**.
# Scope and Limitation
	- The project focuses only on configuring an AWS Lambda function with a specific S3 bucket trigger for text files. The function notifies the admin with the word count everytime a text file is uploaded. Only the IAM Role for the Lambda function was provisioned by AWS specifically for this laboratory. The IAM Role has the policies AWSLambdaBasicExecutionRole, AmazonSNSFullAccess, AmazonS3FullAccess, and CloudWatchFullAccess.
# Implementation
## STEP 1: Configure an SNS topic and subscription
### STEP 1.1: Create an SNS topic
1. Search for *SNS* inside the AWS Management Console.

![unknown_asset](<assets/images/Pasted image 20261019235018.png>)

2. At the left pane, select *Topics* and then Choose *Create topic*.

![unknown_asset](<assets/images/Pasted image 20261019235103.png>)

3. Configure the topic with the following:
	- **Type:** Select *Standard*.
	- **Name:** `word-count-topic`
	- **Display name:** `Broadcasts the word count of a text file`

![unknown_asset](<assets/images/Pasted image 20261019235457.png>)

4. Scroll down and select *Create topic*.
5. Copy the *ARN* to be used later.
### STEP 1.2: Create an SNS subscription
1. Inside the *Amazon SNS* pane, select *Subscriptions*. Select *Create subscription*.

![unknown_asset](<assets/images/Pasted image 20261019235651.png>)

2. Under *Create subscription*, configure with the following details:
	- **Topic ARN:** Select the topic configured at *STEP 1.1*.
	- **Protocol:** Select *Email*.
	- **Endpoint:** `<insert your email>`

![unknown_asset](<assets/images/Pasted image 20261019235836.png>)

3. Select the *Create subscription*.
4. Make sure to confirm the subscription in the email address you provided.
## STEP 2: Setup an S3 bucket
1. Search for *S3* in AWS Management Console.

![unknown_asset](<assets/images/Pasted image 20261020000028.png>)

2. At the left pane, select *General purpose buckets*. and choose *Create bucket*.

![unknown_asset](<assets/images/Pasted image 20261020000112.png>)

3. Under its *General configuration*, follow the configuration:
	- **Bucket type:** Select *General purpose*.
	- **Bucket namespace:** Select *Global namespace*.
	- **Bucket name:** `<unique-bucket-name>`

![unknown_asset](<assets/images/Pasted image 20261020000334.png>)

4. Select *Create bucket*.
## STEP 3: Configure a Lambda function
### STEP 3.1: Deploy a Lambda event function
1. Search for *Lambda* inside the AWS Management Console.

![unknown_asset](<assets/images/Pasted image 20261020000604.png>)

2. At left pane, select *Event Functions*. Then choose *Create Event Function*.

![unknown_asset](<assets/images/Pasted image 20261020000828.png>)

3. Under *Create Event Function*, configure the following:
	- Select *Author from scratch*.
	- **Function name:** `word-counter`
	- **Runtime:** Select *Python 3.14*.

![unknown_asset](<assets/images/Pasted image 20261020000905.png>)

4. Scroll down to *Custom settings*, choose *Additional settings*.

![unknown_asset](<assets/images/Pasted image 20261020001105.png>)

5. Toggle the switch in *Custom execution role*. Select the role provisioned by AWS for this laboratory.

![unknown_asset](<assets/images/Pasted image 20261020001324.png>)

6. Select *Create Event Function*
7. Scroll down to *Runtime settings*. Select *Edit*.

![unknown_asset](<assets/images/Pasted image 20261020001652.png>)

8. Change the *Handler* to `word-counter.lambda_handler` then choose *Save settings.*
9. Under *Code source*, select *Update*. A dropdown will appear and choose *Update from a .zip file*.

![unknown_asset](<assets/images/Pasted image 20261020002616.png>)

10. Upload the zip file version of the [word-counter.py](aws-lambda-scripts/word-counter.py)
11. Observe *line 12*. It is a variable to which the SNS topic ARN is assigned. Paste the *Topic ARN* obtained in **STEP 1.1**. Select *Deploy* after.

![unknown_asset](<assets/images/Pasted image 20261020002605.png>)

### STEP 3.2: Update its general configuration
1. Under *Configuration*, edit the *General configuration*. Choose *Edit*.

![unknown_asset](<assets/images/Pasted image 20261020002747.png>)

2. Under *Edit basic settings*, change the *Timeout* to `1 min`. This is to simply avoid any runtime error. Select *Save* after.

![unknown_asset](<assets/images/Pasted image 20261020002918.png>)

### STEP 3.3: Create a trigger for the Lambda function
1. Under *Function overview*, select *Add trigger*.

![unknown_asset](<assets/images/Pasted image 20261020003029.png>)

2. Select `S3` for the *Trigger Configuration*.

![unknown_asset](<assets/images/Pasted image 20261020003110.png>)

3. Configure the trigger with the following:
	- **Bucket:** `<bucket-name>`
	- **Suffix:** `.txt`
	- Tick the *Recursive invocation*.

![unknown_asset](<assets/images/Pasted image 20261020003141.png>)

![unknown_asset](<assets/images/Pasted image 20261020003157.png>)

## STEP 4: Test the Lambda function
### STEP 4.1: Upload a .txt file
1. Search for *S3* in AWS Management Console.

![unknown_asset](<assets/images/Pasted image 20261020003521.png>)

2. Access the bucket created earlier by clicking its name. 
3. Choose *Upload*.

![unknown_asset](<assets/images/Pasted image 20261020003645.png>)

4. Upload the [test-file.txt](assets/texts/test-file.txt).

![unknown_asset](<assets/images/Pasted image 20261020003718.png>)

5. Choose *Upload*.
6. An email notification should be sent to the email address with the subject `Word Count Results: {text_file_name}` and with the message of `The word count in the {text_file_name} file is {word_count}`.
### STEP 4.2: Upload a .jpg file
1. Upload another file but this time, [aws-s3.jpg](assets/images/aws-s3.jpg). It should not trigger the lambda function.
# Lessons Learned
- The Lambda handler setting (`file-name.lambda_handler`) has to match the file and function name exactly, or the function won’t run or it won't display the program inside the code source.
- **Recursive invocation** is important to understand when dealing with S3 as event trigger. A Lambda function that write objects inside the same S3 bucket may trigger invocation loops causing unexpected costs.
- **VPC** configuration isn't always required for a Lambda function. In this laboratory, a VPC was not used because Amazon S3 and SNS are both public. Assigning a policy of `AmazonS3FullAccess`is sufficient to access S3 objects.