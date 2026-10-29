# Project Title and Summary
## Title: Hosting and Publicly Accessing Objects in Amazon S3 Using Bucket Policies and the AWS CLI
## Project Summary
	- This project covers the basic lifecycle of an object in Amazon S3. Using the AWS CLI from a pre-provisioned EC2 CLI Host, a globally unique S3 bucket was created.Its Block Public Access settings was adjusted and applied a bucket policy that allows public read access to its objects. A JPEG file was uploaded through the S3 console and opened it in a web browser through its Object URL. Finally, the bucket contents were listed with the AWS CLI to confirm the upload from the command line.
## Tech/Skill Used
- **AWS services:** Amazon S3, Amazon EC2 (CLI Host), and EC2 Instance Connect.
- **Tools:** AWS CLI (`aws configure`, `aws s3`, `aws s3api`), Vim, Bash environment variables.
- **Concepts:** Bucket policies (JSON), S3 Block Public Access, global bucket naming, Object URLs, access keys for CLI authentication.
- **Skills:** Command-line administration, writing IAM-style JSON policies, troubleshooting public access, documenting cloud deployments.
# Problem Statement and Objectives
## Problem Statement
	- Applications and websites often need to store files, such as images, and serve them over the internet without managing a server. S3 offers durable, scalable object storage for this, but objects are private by default. To share an object publicly, the bucket’s Block Public Access settings and its bucket policy must both allow it, and the resources must be reachable and verifiable. This project addresses how to create an S3 bucket, make its objects publicly readable in a controlled way, and verify access through both a browser and the AWS CLI.
## Objectives
	- Create an S3 bucket.
	- Upload an object into this bucket.
	- Access the object by using a web browser.
	- List the contents of the S3 bucket by using the AWS Command Line Interface (AWS CLI).
# Architecture Diagram

![unknown_asset](<architecture-diagram/architecture-diagram.png>)

# Scope and Limitation
	- Laboratory focuses on configuration of S3 bucket and the public access of its objects. EC2 instance for the CLI Host has been provisioned along with the networking configurations attached to it. This also used AWS Access Key ID and Secret Keys due to laboratory restrictions of assigning roles.
# Implementation
## STEP 1: Configure AWS CLI
1. Search for *EC2* inside the AWS Management Console.

![unknown_asset](<assets/Pasted image 20261019145923.png>)

2. At navigation pane, select *Instances*
3. Tick the *CLI Host* instance provisioned by AWS and choose *Connect*

![unknown_asset](<assets/Pasted image 20261019145939.png>)

4. Choose *EC2 Instance Connect*
5. Configure the CLI Host with the following configuration:

```Bash
aws configure
```

- **AWS Access Key ID:** `<insert access key>`
- **Secret Key:** `<insert secret key>`
- **Region:** `us-west-2`
- **Output:** `json`
## STEP 2: Create a bucket and its policies
### STEP 2.1: Create and configure S3 bucket
1. Create a global variable for the bucket name. Bucket name should be unique.

```Bash
export BUCKET_NAME=<your-globally-unique-bucket-name>
```

2. Create an s3 bucket.

```Bash
aws s3 mb s3://$BUCKET_NAME
```

Output:
```Bash
make_bucket: <BUCKET_NAME>
```

3. Configure the public access to allow public access via bucket policies.

```Bash
aws s3api put-public-access-block \
    --bucket $BUCKET_NAME \
    --public-access-block-configuration \
	"BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=false,RestrictPublicBuckets=false"
```

### STEP 2.2: Create bucket policies and apply to the S3 bucket
1. Create *JSON* file.

```Bash
vim <file.json>
```

2. Inside the *JSON* file, allow public access to the **S3 bucket objects**.

```JSON
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadForObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::<BUCKET-NAME>/*"
        }
    ]
}
```

- **Sid:** Statement ID used for easier auditing of bucket policies.
- **Effect:** Allow or deny permissions to certain actions.
- **Action:** Specifies allowed or denied things to do in a bucket.
- **Resource:** Specifies to whom the bucket policy is for. (Specific objects or buckets)
3. Apply the bucket policy to the S3 bucket.

```Bash
aws s3api put-bucket-policy \
    --bucket $BUCKET_NAME \
    --policy file://<file.json>
```

## STEP 3: Upload and access an object in the S3 bucket
### STEP 3.1: Upload a JPEG file in the S3 bucket
1. Search for *S3* inside the AWS Management Console.

![unknown_asset](<assets/Pasted image 20261019151145.png>)

2. Choose the S3 bucket created at **STEP 2**.
3. Under *Objects*, select *Upload*.
4. Upload your chosen file.
	**Optional:** Use the [aws-s3](/assets/aws-s3.jpg) picture.
### STEP 3.2: Access the object
1. Select the desired object uploaded inside the bucket.

![unknown_asset](<assets/Pasted image 20261019151443.png>)

2. Copy its *Object URL*.
3. In any browser, paste the *Object URL*. It should look like this.

![unknown_asset](<assets/Pasted image 20261019151551.png>)

4. To further verify, inside **AWS CLI** run the program to get the list of objects inside the S3 bucket.

```Bash
aws s3 ls s3://$BUCKET_NAME
```

# Lessons Learned
- For **Public Access**, it is required to have two of the **Block Public Access** unticked. These are the `BlockPublicPolicy` and `RestrictPublicBuckets` to ensure that public policies would take effect.
- The trailing `/*` in the **Resource** is important. It targets all the **bucket objects** specifically instead of the bucket itself.
- The policy `Version` is a language version, not a date. `"2012-10-17"` is the policy language version and should be kept exactly as written. Changing it to the current date will cause errors or disable policy features.
- `aws s3` can access the configured region inside `aws configure` unlike `aws s3api`. It is important