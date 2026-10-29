# Project Title and Summary
## Title: Deploying a Cafe and Bakery Static Website to Amazon S3
## Project Summary
	- This project hosts a pre-built café and bakery website, consisting of HTML, CSS, and image files provided by AWS, as a static website on Amazon S3. Using the AWS Command Line Interface (CLI) through AWS Systems Manager Session Manager, an S3 bucket was created, the website files were uploaded, and static website hosting was enabled. To streamline maintenance, a Bash script was developed to automate deployment, so that changes committed to the website are published to the S3 bucket.
## Tech/Skill Used
### AWS Services
#### Amazon S3
	- Bucket creation, object uploads, and static website hosting
#### Amazon EC2
	- Access to AWS CLI via Sessions Manager
### Tools
#### AWS CLI
	- aws s3api, aws s3 website, aws s3 sync, aws iam attach-user-policy, aws iam create-user, and aws iam create-login-profile
	- Linux command line for navigating directories, downloading files, unzipping files, and creating bash script
# Problem Statement and Objectives
## Problem Statement
	- A cafe and bakery needs an online presence so customers can see its menu, location, and offerings. A traditional web server adds ongoing costs, patching, and capacity planning that a small business with a simple, mostly unchanging site does not need. The business needs hosting that is affordable, highly available, and easy to maintain. Deployment should also be secure, scriptable, and repeatable, so updates can be pushed with a few CLI commands without exposing management ports on a server.
## Objectives
	- Run AWS CLI commands that use IAM and Amazon S3 services.
	- Deploy a static website to an S3 bucket.
	- Create an IAM user that has full access to Amazon S3.
	- Create a script that uses AWS CLI to copy files in local directory to Amazon S3 for faster deployment.
# Architecture Diagram

![unknown_asset](<architecture-diagram/architecture-diagram.png>)

# Scope and Limitation
	- This project focuses on deployment of a static website via Amazon S3. Configuration of the EC2 Instance along with its security group and VPC are provisioned by AWS. Secret Access Key and Access Key ID were given instead of an IAM role in accessing AWS CLI.
# Implementation
## Step 1: Connect to Amazon Linux EC2 instance
1. Search for *EC2* in the AWS Management Console.

![unknown_asset](<assets/Pasted image 20261014000917.png>)

2.  Navigate to *Instances* located at the left pane.

![unknown_asset](<assets/Pasted image 20261014000953.png>)

3. Choose or create your own CLI host instance.
4. Click on *Connect.* A new tab will appear.

![unknown_asset](<assets/Pasted image 20261014001018.png>)

5. Select the *SSM Session Manager.*

![unknown_asset](<assets/Pasted image 20261014001039.png>)

## Step 2: Configure AWS CLI
1. Though not recommended, use Access Key ID and Secret Access Key given by AWS.

```Bash
aws configure
```

- **AWS Access Key ID:** `<access key id>`
- **AWS Secret Access Key:** `<secret access key>`
- **Default region name:** `us-west-2`
- **Default output format:** `json`
## Step 3: Create an S3 bucket using AWS CLI
1. Create an S3 bucket. Change `<bucket-name>` to desired name for S3 bucket.

```Bash
aws s3api create-bucket --bucket <bucket-name> --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2
```

```Bash
# Output should look like this
{
	 "Location": "http://<bucket-name>.s3.amazonaws.com/"
}
```

## Step 4: Create a new IAM user that has full access to Amazon S3
1. Create a new IAM user. Change `<new-user>` to desired username.

```Bash
aws iam create-user --user-name <new-user>
```

2. Set a login profile for the IAM user.  Change `<new-user>` and `<user-password>`

```Bash
aws iam create-login-profile --user-name <new-user> --password <user-password>
```

3. Attach an IAM user policy that grants the user full access to Amazon S3.

```Bash
aws iam attach-user-policy --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess --user-name <new-user>
```

4. Attempt to access the IAM user.
	**Note:** Copy the 12 digit Account ID number located at the top right corner of the AWS Console.
## Step 5: Adjust S3 bucket permissions
1. On AWS Management Console, on Amazon S3 bucket, choose the `<bucket-name>`.

![unknown_asset](<assets/Pasted image 20261013234730.png>)

2. Go to permissions  and under *Block public access,* select *Edit.*

![unknown_asset](<assets/Pasted image 20261013234812.png>)

![unknown_asset](<assets/Pasted image 20261013234839.png>)

3. Untick *Block all public access* but tick the first two. Save changes.

![unknown_asset](<assets/Pasted image 20261014000141.png>)

4. Still on *permissions tab,* under *Bucket policy* choose *Edit.*

![unknown_asset](<assets/Pasted image 20261014000221.png>)

5. Enter the JSON text below to grant only *GetObject* action to the public.

```JSON
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadForWebsite",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::<bucket-name>/*"
        }
    ]
}
```
 
## Step 6: Extract website files
1. Back in SSH terminal, extract the zip file that was provisioned by AWS. Otherwise, create one.

```Bash
cd <file-path>
tar xvzf static-website-v2.tar.gz
cd static-webiste
```

## Step 7: Upload files to Amazon S3 Bucket
1. Configure the S3 bucket to host a static website with an index document named index.html.

```Bash
aws s3 website s3://<bucket-name>/ --index-document index.html
```

2. Upload the files to the S3 bucket.

```Bash
aws s3 cp <file-path>/static-website/ s3://<bucket-name>/ --recursive
```

3. Verify if files were uploaded.

```Bash
aws s3 ls s3://<bucket-name>
```

4. In AWS Management Console, on the S3 bucket details, of `<bucket-name>` select *Properties* and scroll down to *Static website hosting* to copy the *Bucket website endpoint.*

![unknown_asset](<assets/Pasted image 20261014000725.png>)

![unknown_asset](<assets/Pasted image 20261014000827.png>)

5. Verify that the static website is running.
## Step 8: Create a batch file for updating website
1. Create and edit a bash script file that enables uploading of local files to the S3 bucket. To save the file, hit *ESC* and `:wq`.

```Bash
vim <bash-script-file.sh>
```

```Bash
#!/bin/bash
aws s3 sync <file-path>/static-website/ s3://<bucket-name>/
```

2. Make the file executable.

```Bash
chmod +x <bash-script-file.sh>
```

3. Simulate a change in the html file.
4. Run the bash script.

```Bash
./<bash-script-file.sh>
```

5. Check the S3 bucket via endpoint if changes were successfully uploaded.
# Lessons Learned
- Amazon S3 Access Control List (ACL) is a legacy file-by-file security granting read and write permission to each objects and buckets. It defines which AWS accounts or group can perform certain actions. 
- In the industry, bucket policies are recommended as they eliminate the need to manually change the permission for thousands of files.
- The `cp` command in the context of uploading to S3 bucket, copies and overwrites the existing objects in the S3 even if only minor changes were committed. In contrast, `sync` compares each local file with the S3 object and only uploads those changes.