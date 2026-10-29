# Project Title and Summary
## Title: Designing a Multi-AZ VPC and Hosting a Public Web Server on AWS
## Project Summary
	- Built a custom VPC with public and private subnets across two Availability Zones, configured internet and NAT routing, and deployed a web server secred by a security group.
## Tech/Skills Used
	- Amazon VPC, EC2 Instance, Subnets, Route Tables, Internet Gateway, NAT Gatewat, Security Groups, and CIDR Planning.
# Problem Statement and Objectives
## Problem Statement
	- The need for a network that is isolated by default but exposes only what must be public.
## Objectives
	- Utilize AWS's "VPC and more" configuration for the first Availability Zone.
	- Manually create the second Availability Zone's public and private subnets and add to the same VPC.
	- Launch a web server in Public Subnet 2 with appropriate security group.
	- Verify that web server is reachable from the internet.
# Architecture Diagram

![unknown_asset](<architecture-diagram/architecture-diagram.png>)

# Network Consideration and Limitation
	- IP Addresses along with CIDR were stated as a requirement in the laboratory.
	- NAT Gateway is at public subnet to route to Internet Gateway.
	- Two Availability Zone are for high availability and fault tolerance in the design.
	- Website is given in the form of s3 object automatically provisioned.
# Implementation
## Step 1: Create Initial VPC
1. In AWS Management Console, search for *VPC*.

![unknown_asset](<assets/Pasted image 20261011142348.png>)

2. Choose *Your VPCs* located at the left panel.

![unknown_asset](<assets/Pasted image 20261011160326.png>)

3. At the main window, choose *Create VPC*. 

![unknown_asset](<assets/Pasted image 20261011160516.png>)

4. Inside Create VPC, select the option *VPC and more* and enable **Auto-generate** under *Name tag auto-generation*.

![unknown_asset](<assets/Pasted image 20261011160854.png>)

5. Under *IPv4 CIDR block*, use the IP Address `10.0.0.0/16` and select *No IPv6 CIDR block*.

![unknown_asset](<assets/Pasted image 20261011161023.png>)

6. Select 1 Under *Number of Availability Zones* and associate to `us-west-2a`
	**Note:** To see us-west-2a double check if you are in the region us-west-2 (Oregon).

![unknown_asset](<assets/Pasted image 20261011161255.png>)

7. Under *Number of public subnets and Number of private subnets,* choose only 1 for each and configure the following:
- **Public subnet CIDR block:** `10.0.0.0/24`
- **Private subnet CIDR block:** `10.0.1.0/24`

![unknown_asset](<assets/Pasted image 20261011161523.png>)

8. In *Preview Pane,* edit the name of the following:
- **VPC:** `Lab-VPC`
- **Public Subnet:** `Public Subnet 1`
- **Private Subnet:** `Private Subnet 1`
- **Internet Gateway:** `Lab-IGW`
- **NAT Gateway:** `Lab-NAT-GW`

![unknown_asset](<assets/Pasted image 20261011161618.png>)

![unknown_asset](<assets/Pasted image 20261011161644.png>)

9. Double check the VPC settings then click on **Create VPC**
## Step 2: Create Additional Subnet
1. Still under *VPC,* choose *Subnets* at the left panel to create the remaining subnets.

![unknown_asset](<assets/Pasted image 20261011162057.png>)

2. At the main window, click on *Create subnet*.

![unknown_asset](<assets/Pasted image 20261011162146.png>)

3. For the first subnet, use the following configuration:
- **VPC ID:** `Lab-VPC`
- **Subnet name:** `Public Subnet 2`
- **Availability Zone:** `us-west-2b`
- **IPv4 subnet CIDR block:** `10.0.2.0/24`
- **IPv6 CIDR block:** No IPv6 CIDR

![unknown_asset](<assets/Pasted image 20261011162618.png>)

![unknown_asset](<assets/Pasted image 20261011162707.png>)

4, Add another subnet with the following configuration:
- **Subnet name:** `Private Subnet 2`
- **Availability Zone:** `us-west-2b`
- **IPv4 subnet CIDR block:** `10.0.3.0/24`
- **IPv6 CIDR block:** No IPv6 CIDR

![unknown_asset](<assets/Pasted image 20261011162742.png>)
## Step 3: Associate the Subnets and Add Routes
1. In *VPC,* find *Route tables* located at the leftmost panel.

![unknown_asset](<assets/Pasted image 20261011163812.png>)

2. Tick the **Public Route Table** created earlier during the VPC and more. Details of the route table will appear.

![unknown_asset](<assets/Pasted image 20261011163906.png>)

3. Select *Subnet associations* and Edit the *Explicit subnet associations*.

![unknown_asset](<assets/Pasted image 20261011164002.png>)

4. Make sure that both *Public Subnet* are ticked.

![unknown_asset](<assets/Pasted image 20261011164236.png>)

5. Repeat **Steps 3.2 - 3.4** but for *Private Routing Table*.

![unknown_asset](<assets/Pasted image 20261011164338.png>)

**Optional:** Double check the resource map of the VPC. It should look like:
- private subnets -> private routing table -> NAT gateway
- public subnets -> public routing table -> internet gateway
## Step 4: Create a VPC Security Group
1. Under VPC, choose *Security groups* located at the left side panel.

![unknown_asset](<assets/Pasted image 20261011164729.png>)

2. At the main window, select *Create security group*.

![unknown_asset](<assets/Pasted image 20261011164925.png>)

3. In security group configuration, follow the following:
- **Security group name:** `Lab-SG`
- **Description:** `Allow HTTP Access`
- **VPC:** `Lab-VPC`
- **Inbound rules:** `HTTP`

![unknown_asset](<assets/Pasted image 20261011165421.png>)

## Step 5: Launch the Web Server Instance
1. Search for *EC2* in AWS Management Console.

![unknown_asset](<assets/Pasted image 20261011165542.png>)

2. At the left side panel, select *Instances*.

![unknown_asset](<assets/Pasted image 20261011165616.png>)

3. Located at the main window, choose *Launch instances*

![unknown_asset](<assets/Pasted image 20261011165700.png>)

4. For EC2 instance configuration, use the following:
- **Name:** `Web Server 1`
- **Amazon Machine Image:** Amazon Linux 2023
- **Instance type:** t3.micro

![unknown_asset](<assets/Pasted image 20261011165844.png>)

![unknown_asset](<assets/Pasted image 20261011165905.png>)

![unknown_asset](<assets/Pasted image 20261011170011.png>)

5. Under *Key pair (login),* though not recommended, select *Proceed without a key pair* because the goal is the simply launch a web server one time.

![unknown_asset](<assets/Pasted image 20261011170141.png>)

6. Under *Network settings,* Use the following:
- **VPC:** *Lab-VPC*
- **Subnet:** *Public Subnet 2*
- **Auto-assign public IP:** Enable
- **Select existing security group:** `Lab-SG`

![unknown_asset](<assets/Pasted image 20261011170601.png>)

7. Select *Additional Configuration* and under *User data,* write the following to create the website:
	**Note:** `<link to s3 object>` was provided by the AWS.

```Bash
#!/bin/bash
# Update package managers and install Apache, MariaDB, and PHP

dnf install -y httpd mariadb105-server php php-mysqli

# Download and unzip the target lab deployment files

wget <link to s3 object>
unzip lab-app.zip -d /var/www/html/

# Start the services and confgure them to turn on automatically at boot
systemctl enable httpd
systemctl start httpd
```

## Step 6: Access the Web Server Instance
1. Under EC2 instances, tick the *Web Server 1* and in its details, find and copy the *Public IPv4 address*.

![unknown_asset](<assets/Pasted image 20261011171302.png>)

2. Copy and paste the Public IPv4 address to any browser.
	**Note:** Make sure that it is in *http://*.

![unknown_asset](<assets/Pasted image 20261011171553.png>)

# Lessons Learned
- A newly created subnet does not automatically have an internet access. To make it public, it should be manually configured to a routing table that contains **0.0.0.0/0** with a destination to an **internet gateway**.
- Assigning a public IP address to an EC2 instance in a private subnet does not grant an access to the instance via the internet.
- **User data runs only once** at the moment the EC2 instance is launched. Any future reboots, stops or starts will not trigger the script.
- By default, any new subnet is **implicitly tied** to the VPC's Main Route Table. Best practice would be to include it in explicit route table association.