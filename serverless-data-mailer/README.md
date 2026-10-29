# Project Title and Summary
## Title: Automated Daily Sales Analysis Reports for a Café Using AWS Lambda, Amazon SNS, and Amazon EventBridge
## Project Summary
	- This project automates the daily sales reporting for a café website. Two serverless AWS Lambda functions do the work. The first, `salesAnalysisReportDataExtractor`, connects to the café’s MySQL (MariaDB) database inside a VPC, using the PyMySQL library packaged as a Lambda layer, and extracts the sales data. The second, `salesAnalysisReport`, calls the extractor, formats the results into a report, and publishes it to an Amazon SNS topic, which emails the report to a subscriber. An Amazon EventBridge schedule triggers the report function every day, so nobody has to run it manually. Amazon CloudWatch logs were used to troubleshoot errors along the way.
## Tech/Skill Used
### AWS Services
	- AWS Lambda (functions and layers)
	- Amazon SNS (topic and email subscription)
	- Amazon EventBridge (scheduled cron trigger)
	- AWS IAM (execution roles and policies)
	- AWS Systems Manager Parameter Store (database credentials)
	- Amazon VPC, subnets, and security groups (private database access)
	- Amazon EC2 (café website and CLI host)
	- Amazon CloudWatch (logs and troubleshooting)
### Tools and Languages
	- Python (Lambda runtime)
	- PyMySQL (external library)
	- MySQL/MariaDB
	- AWS CLI
	- JSON (test events)
# Problem Statement and Objectives
## Problem Statement
	-The café owner needs to know how the business is performing, but sales data sits in a database that only shows up when someone queries it by hand. Pulling the numbers, formatting them, and sending them out every day is repetitive and easy to forget. Running a dedicated server just for a short daily task would also waste money, because it would sit idle most of the day. The project addresses the problem through an automation utilizing AWS Lambda.
## Objectives
	- Recognize necessary AWS IAM policies to facilitate a Lambda function to other AWS resources.
	- Create a Lambda layer to satisfy an external library dependency.
	- Create a Lambda function that extracts data from database and send reports to user.
	- Deploy and test a Lambda function that is initiated based on a schedule and that invoked another function.
	- Use CloudWatch to perform troubleshooting.
# Architecture Diagram

![unknown_asset](<architecture-diagram/architecture-diagram.png>)

# Scope and Limitation
	- AWS has provisioned everything that is not directly related to the project as this was conducted in a controlled environment. These include the following:
		- EC2 LAMP instance
		- MariaDB Instance (Inside EC2)
		- VPC
		- Subnet
		- Security Group
		- IAM Roles
		- Parameters in parameter store
		- Lambda source code and libraries
		- Cafe Website
	- The project focuses on deployment of a Lambda function that is scheduled to run at a specific time. Thus, this will produce two Lambda function and an SNS service for the notification.
# Implementation
## Step 1: Create a Lambda layer and a data extractor Lambda function.
1. Download the project files required to create the project.
	
	[pymysql-v3](pymysql-v3)
	
	[salesAnalysisReportDataExtractor.py](aws-lambda-scripts/salesAnalysisReportDataExtractor.py)
	
	**Note:** The **salesAnalysisReportDataExtractor.zip** file is a Python implementation of a Lambda function that makes use of the PyMySQL open-source client library to access the MySQL café database. Library has been packaged as **pymysql-v3**. Download both and compress to zip file.
### Step 1.1: Creating a Lambda layer
1. Search for *Lambda* in AWS Console.

![unknown_asset](<assets/Pasted image 20261017161631.png>)

2. At left pane, select *Layer* and at the upper right, choose *Create layer*.

![unknown_asset](<assets/Pasted image 20261017161753.png>)

2. Configure the following layer settings:
	- For **Name**, enter `pymysqlLibrary`
    - For **Description**, enter `PyMySQL library modules`.
    - Select *Upload a .zip file*. To upload the pymysql-v3.zip file, choose *Upload*, navigate to the folder where you downloaded the pymysql-v3.zip file, and open it.
    - For *Compatible runtimes*, choose **Python 3.14**.
		**Note:** Remember to zip the files before uploading.

![unknown_asset](<assets/Pasted image 20261017161912.png>)

3. Choose **Create**.
### Step 1.2: Create a data extractor Lambda function
1. At the navigation pane, choose *Functions* and choose *Create function*.

![unknown_asset](<assets/Pasted image 20261017163121.png>)

2. Configure the following options:
	- At the top of the *Create function* page, select *Author from scratch*.
	- For *Function name*, enter `salesAnalysisReportDataExtractor`
	- For *Runtime*, choose *Python 3.14*.
	- Expand *Additional settings*, and configure the following options:
	    - For *Custom execution role*, choose *Use an existing role*.
	    - For Existing role:, choose *salesAnalysisReportDERole*.

![unknown_asset](<assets/Pasted image 20261017163203.png>)

![unknown_asset](<assets/Pasted image 20261017163223.png>)

![unknown_asset](<assets/Pasted image 20261017163237.png>)

### Step 1.3: Adding the Lambda layer to the function
1. In the *function overview* panel, choose *Layers*.

![unknown_asset](<assets/Pasted image 20261018095106.png>)

2. Select *Add a layer*.

![unknown_asset](<assets/Pasted image 20261018095152.png>)

3. On the *Add layer* page, configure the following:
	- **Choose a layer:** Choose *Custom layers*.
	- **Custom layers:** Select *pymysqlLibrary*.
	- **Version:** Choose *1*.

![unknown_asset](<assets/Pasted image 20261018095234.png>)

4. Choose *Add*.
### Step 1.4: Importing the code for the data extractor Lambda function
1. Inside the *Event Function* overview, scroll down to *Runtime settings* and Choose *Edit*.

![unknown_asset](<assets/Pasted image 20261018095533.png>)

2. For the *Handler*, enter `salesAnalysisReportDataExtractor.lambda_handler`.
	**Note:** Handler name consists of the Python module path and the main function to run. `<filename.main-function>`. 
3. Choose *Save*.
4. In the *Code source* panel, choose *Update*.
5. Choose *.zip file*.
6. Choose *Choose file*, and then navigate to and select the *salesAnalysisReportDataExtractor.zip* file downloaded earlier.

![unknown_asset](<assets/Pasted image 20261018101925.png>)

7. Choose **Save**.

![unknown_asset](<assets/Pasted image 20261018101949.png>)

### Step 1.5: Configuring network settings for the function
1. Under *Configuration* tab, select *VPC* and click on *Edit*.

![unknown_asset](<assets/Pasted image 20261018102042.png>)

2. In the *Edit VPC* panel, configure the following:
	- **VPC:** Select the VPC.
	- **Subnets:** Select the subnet.
	- **Security groups:** Select the security group.
	**Note:** AWS has provisioned the VPC, subnet and security group for the laboratory as this is in a controlled setup.

![unknown_asset](<assets/Pasted image 20261018102134.png>)

3. Add the MySQL/Aurora in the inbound rules of the security group to enable the Lambda function to interact with the database.
4. Choose *Save*.
## Step 2: Testing the data extractor Lambda function
	- It is necessary to manually obtain the value from the Parameter Store as the salesAnalysisDataExtractor function does not automatically do this in its Source Code.
### Step 2.1: Launching a test of the Lambda function
1. In the *Search  bar*, type the *Systems Manager*.

![unknown_asset](<assets/Pasted image 20261018105417.png>)

2. In its navigation pane, choose *Parameter Store*.

![unknown_asset](<assets/Pasted image 20261018105437.png>)

3. Choose each of the following parameter names, and copy paste the Value of each one into a text editor document.
	- **/cafe/dbUrl**
	- **/cafe/dbName**
	- **/cafe/dbUser**
	- **/cafe/dbPassword**
4. Return to the *Lambda Management Console*. On the *salesAnalysisReportDataExtractor* function, select on the *Test* tab.
5. Configure the *Test event* panel in the  following configuration:
	- **Test event action:** Select *Create new event*.
	- **Invocation type:** Select *Synchronous*.
	- **Event name:** `SARDETestEvent`
	- **Template:** Choose *hello-world*.
	- **Event JSON:**

```JSON
{
	 "dbUrl": "<value of /cafe/dbUrl parameter>",
	 "dbName": "<value of /cafe/dbName parameter>",
	 "dbUser": "<value of /cafe/dbUser parameter>",
	 "dbPassword": "<value of /cafe/dbPassword parameter>"
 
}
```

![unknown_asset](<assets/Pasted image 20261018105336.png>)

6. Choose *Save* and then *Test*.

![unknown_asset](<assets/Pasted image 20261018105504.png>)

![unknown_asset](<assets/Pasted image 20261018110040.png>)

**Note:** Body is still empty as the database has no data.

### Step 2.2: Placing an order and testing again
1. To obtain the IP address of the Cafe Website, go to *EC2*.

![unknown_asset](<assets/Pasted image 20261018110316.png>)

2. In *EC2 Service*, choose *Instances*.
3. Tick the instance where the website is hosted.
4. Under its details, find the *Public IPv4 address*.
5. Go back to the Lambda function and run the test event.

![unknown_asset](<assets/Pasted image 20261018110550.png>)

## Step 3: Configuring notifications
### Step 3.1: Creating an SNS topic
1. In *AWS Console*, search for *SNS*.

![unknown_asset](<assets/Pasted image 20261018212314.png>)

2. At the navigation pane, select *Topics* and *Create topic*.

![unknown_asset](<assets/Pasted image 20261018212326.png>)

3. Under *Create topic*, configure the following:
	- **Type:** Choose *Standard*.
	- **Name:** `salesAnalysisReportTopic`
	- **Display name:** `SARTopic`

![unknown_asset](<assets/Pasted image 20261018212343.png>)

3. Click on *Create topic*.
4. Copy the *ARN* to be used later in the lambda function.
### Step 3.2: Subscribing to the SNS topic
1. Under the *Amazon SNS* topic, select the *Subscription* at its left panel. Select *Create subscription* located at the main window.

![unknown_asset](<assets/Pasted image 20261018212523.png>)

2. Under the *Create subscription* configure:
	- **Protocol**: Choose *Email*.
    - **Endpoint**: Enter an email address that you can access.

![unknown_asset](<assets/Pasted image 20261018212543.png>)

3. Choose *Create subscription*.
    The subscription is created and has a **Status** of _Pending confirmation_.
4. Check the inbox for the email address that you provided.
    You should see an email from SARTopic with the subject "AWS Notification - Subscription Confirmation."
5. Open the email, and choose *Confirm subscription*.
    A new browser tab opens and displays a page with the message "Subscription confirmed!"
## Step 4: Creating the salesAnalysisReport Lambda function
	- With how the laboratory was configured, the zip file for the salesAnalysisReport is stored inside the EC2 Instance to be provisioned via AWS CLI.

**salesAnalysisReport:** [salesAnalysisDataReport](aws-lambda-scripts/salesAnalysisDataReport.py)

**Note:** Similar to the other files, compressed it to a zip file. If you created your own lambda function, skip to **Step 4.4**.
### Step 4.1: Connecting to the CLI Host instance
1. Search for *EC2* in the AWS Console.

![unknown_asset](<assets/Pasted image 20261018213427.png>)

2. At left pane, select *Instances* and tick the target CLI Host Instance.
3. At the upper right of the main window, choose *Connect*.
4. Under *Choose how to connect*, select *EC2 Instance Connect*.

![unknown_asset](<assets/Pasted image 20261018213555.png>)

### Step 4.2: Configuring the AWS CLI
With the restrictions of the laboratory setup, Access Key and Secret Access Key were used to authenticate the connection as an IAM User.

1. Configure the following:

```Bash
aws configure
```

- **AWS Access Key ID**: At the top of these instructions, choose the Details dropdown menu, and then choose Show. A *Credentials* window opens. From this window, copy the *AccessKey* value, paste it into the terminal window, and press Enter.
- **AWS Secret Access Key**: From the same *Credentials* window, copy the *SecretKey* value, paste it into the terminal window, and press Enter.
- **Default region name**: Enter the Region code for the Region where you created the previous Lambda function. For this lab, enter the `us-west-2` Region code into the terminal window, and press Enter. To find this code, in the upper-right menu of the Lambda management console, choose the Region dropdown menu.
- **Default output format**: Enter `json` and press Enter.
### Step 4.3: Creating the salesAnalysisReport Lambda function using the AWS CLI
1. To verify that the salesAnalysisReport-v2.zip file containing the code for the salesAnalysisReport Lambda function is already on the CLI Host, run the following commands in the terminal:

```Bash
cd activity-files
ls
```

2. Next, use the Lambda create-function command to create the Lambda function and configure it to use the salesAnalysisReportRole IAM role.

```Bash
aws lambda create-function \
	--function-name salesAnalysisReport \
	--runtime python3.14 \
	--zip-file fileb://salesAnalysisReport-v2.zip \
	--handler salesAnalysisReport.lambda_handler \
	--region <region> \
	--role <salesAnalysisReportRoleARN>
```

### Step 4.4: Configuring the salesAnalysisReport Lambda function
1. Open the Lambda management console.
2. Choose **Functions**, and then choose **salesAnalysisReport**.
    The **Details** page for the function opens.
3. Review the details in the **Function overview** and **Code source** panels for the created function.
    **Note:** On line 26 that the function retrieves the ARN of the topic to publish to, from an environment variable named **topicARN**. Therefore, you need to define that variable in the **Environment variables** panel.
4. Choose the **Configuration** tab, and choose **Environment variables**.

![unknown_asset](<assets/Pasted image 20261018214807.png>)

5. Choose **Edit**.
6. Choose **Add environment variable**, and configure the following options:
    - **Key**: Enter `topicARN`
    - **Value**: Paste the ARN value of the salesAnalysisReportTopic SNS topic that you copied earlier.
7. Choose **Save**.
    The following message appears: "Successfully updated the function salesAnalysisReport."
### Step 4.5: Testing the salesAnalysisReport Lambda function
1. Choose the **Test** tab, and configure the test event as follows:
    - For **Test event action**, choose **Create new event**.
    - For **Event name**, enter `SARTestEvent`
    - For **Template**, choose **hello-world**.
    The function does not require any input parameters. Leave the default JSON lines as is.

![unknown_asset](<assets/Pasted image 20261018215041.png>)

2. Choose **Save**.
3. Choose **Test**.

![unknown_asset](<assets/Pasted image 20261018215205.png>)

4. To troubleshoot the error, adjust the *Timeout*. *Configuration > General Configuration > Edit*. Adjust the timeout as needed.

![unknown_asset](<assets/Pasted image 20261018215355.png>)

4. Once successful, check your email inbox.

![unknown_asset](<assets/Pasted image 20261018215409.png>)

5. Try adding data to the database and run the test to verify if lambda function is working as intended.
### Step 4.6: Adding a trigger to the salesAnalysisReport Lambda function
1. To add a trigger, go to *Function overview* and choose *Add trigger*.

![unknown_asset](<assets/Pasted image 20261018215539.png>)

2. Configure the trigger with the following information:
	- In the **Trigger configuration** pane, from the dropdown list, choose *EventBridge (CloudWatch Events)*.
	- For **Rule**, choose *Create a new rule*.
	- For **Rule name**, enter `salesAnalysisReportDailyTrigger`
	- For **Rule description**, enter `Initiates report generation on a daily basis`
	- For **Rule type**, choose **Schedule expression**.
	- For **Schedule expression**, specify the schedule that you would like by using a Cron expression.

![unknown_asset](<assets/Pasted image 20261018215633.png>)

3. Choose *Add*.
4. Wait until the scheduled time, and then check your email inbox.
# Lessons Learned
- **AWS Lambda function** has no permission of its own. It borrows permission to access certain AWS services through **IAM Roles**.
- **Lambda Layers** keep libraries separate from the code. This helps in ensuring that the function code is small and that libraries inside layers can be reused by other functions.
- The **handler** must be written as `filename.function_name` (e.g. `salesAnalysisReportDataExtractor.lambda_handler`). If the filename or function name is off by one character, Lambda cannot find the code.
- The report function does not send emails itself. It publishes a message to an **SNS topic**, and SNS delivers it to every subscriber. Adding another recipient later takes a new subscription, not a code change.
- **EventBridge** scheduler allows automation of the lambda function based on time. Though the EventBridge used in the laboratory is a legacy.
- Everytime a function is run, it writes logs to CloudWatch automatically. This is allowed by the policy `AWSLambdaBasicExecutionRole`.