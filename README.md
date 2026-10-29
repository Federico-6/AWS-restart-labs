# AWS Projects

This repository contains beginner-friendly projects and practice exercises focused on Amazon Web Services (AWS), cloud infrastructure, databases, networking, and a small Python program. Each project has its own folder with a README, diagrams, screenshots, or code where applicable.

## Projects

### 1. [Auto Scaling Group](auto-scaling-group/)
This project sets up a web application using an Application Load Balancer and an EC2 Auto Scaling Group. The load balancer sends traffic to the available servers, while the Auto Scaling Group can add or remove EC2 instances as demand changes. The project demonstrates how AWS can help keep a website available and adjust its capacity.

### 2. [Hosting Public Files with Amazon S3](aws-s3-public-hosting/)
This project shows how to store a file in an Amazon S3 bucket and make it publicly accessible using a bucket policy. It also uses the AWS Command Line Interface (AWS CLI) to create the bucket, upload a file, and check the stored objects. It introduces basic S3 permissions and object URLs.

### 3. [Deploying a VPC and EC2 Instance with CloudFormation](cloudformation-vpc-ec2/)
This project uses an AWS CloudFormation template to create cloud resources from a YAML file instead of setting them up one by one in the console. The template describes a Virtual Private Cloud (VPC), networking resources, a security group, and an EC2 instance. It introduces the idea of managing infrastructure through reusable configuration files.

### 4. [Migrating MariaDB from EC2 to Amazon RDS](ec2-to-rds-mariadb-migration/)
This project moves a MariaDB database from an EC2 server to Amazon RDS, AWS's managed relational database service. It covers preparing the network, creating the RDS database, exporting and importing the existing data, and updating the café website to connect to the new database. The goal is to separate the database from the web server.

### 5. [Finding Prime Numbers with Python](prime-numbers-python/)
This small Python program asks the user for a range of numbers, finds the prime numbers within that range, and saves the results to a text file. It is a basic programming exercise that practices user input, loops, conditions, and writing output to a file.

### 6. [Creating and Querying an Amazon Aurora Database](rds-aurora-provision-and-query/)
This project introduces Amazon Aurora, a managed relational database compatible with MySQL. It covers setting up a database environment, connecting to the database through an EC2 instance, and running SQL statements to create tables, add sample data, and query records. The folder includes SQL files and an architecture diagram.

### 7. [Route 53 DNS Failover Routing](route53-failover-routing/)
This project configures Amazon Route 53 to direct visitors to a backup website if the primary website becomes unavailable. A health check monitors the primary site, while CloudWatch and SNS provide monitoring and email notifications. It demonstrates one way to improve website availability using two EC2 instances in different Availability Zones.

### 8. [Automated Daily Sales Reports](serverless-data-mailer/)
This project automates the creation and delivery of daily sales reports for a café. AWS Lambda functions retrieve sales data from a database and prepare a report, while Amazon SNS sends the report by email. Amazon EventBridge schedules the process to run automatically, reducing the need to generate the report manually.

### 9. [Automatic Word Count for S3 Text Files](serverless-s3-wordcount-notifier/)
This project counts the words in a text file whenever a `.txt` file is uploaded to an Amazon S3 bucket. An AWS Lambda function processes the file, and Amazon SNS sends the word count to an email subscriber. It demonstrates how AWS services can work together in response to an event without needing a continuously running server.

### 10. [Hosting a Static Website on Amazon S3](static-website-s3/)
This project publishes a café and bakery website using Amazon S3 static website hosting. The website's HTML, CSS, and image files are uploaded to an S3 bucket, and a Bash script using the AWS CLI helps copy updated files to the bucket. It introduces a simple way to host a website that does not require a web server.

### 11. [Multi-AZ VPC and Public Web Server](vpc-multi-az-architecture/)
This project builds a Virtual Private Cloud (VPC) with public and private subnets across two Availability Zones. It configures routing, an Internet Gateway, a NAT Gateway, and security groups, then places a web server in a public subnet. The project introduces basic AWS networking and shows how resources can be arranged across Availability Zones.

## Repository Notes

- Each AWS project folder contains its own instructions and supporting files where available.
- Some projects were completed in a guided lab environment and may depend on resources that were already provided.
- Running these projects in your own AWS account may create charges. Review the resources you create and remove them when you finish testing.
- Do not commit AWS access keys, passwords, database credentials, or other secrets to the repository.
