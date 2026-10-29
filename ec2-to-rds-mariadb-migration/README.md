# Project Title and Summary
## Title: Migrating a MariaDB Database from Amazon EC2 to Amazon RDS Using the AWS CLI
## Project Summary
	- This project migrates the database of a Cafe web application from a MariaDB instance hosted on the same EC2 server as the website to a managed Amazon RDS for MariaDB instance. Using the AWS CLI, the network prerequisites (a security group, two private subnets, and a DB subnet group) were created, followed by the provisioning of the RDS instance. The existing `cafe_db` database was then exported with `mysqldump` and imported into RDS over an SSL/TLS connection. Finally, the website was reconfigured to use the new database through AWS Systems Manager Parameter Store, and the cutover was validated by submitting a new order and confirming that it was recorded in RDS.
## Tool/Skill Used
### Tools and Services
	- Amazon EC2 and EC2 Instance Connect
	- AWS CLI
	- Amazon RDS for MariaDB
	- Amazon VPC (subnets, security groups, route tables)
	- AWS Systems Manager Parameter Store
	- `mysqldump` and `mysql` client
	- Amazon RDS CA certificate bundle (SSL/TLS)
### Skills
	- Provisioning managed databases through the CLI
	- Network isolation and least-privilege security groups
	- Database backup, export, and import
	- Application configuration without code changes
	- Data validation after migration
# Problem Statement and Objectives
## Problem Statement
	- The Cafe website stores its order data in a MariaDB database on the same EC2 instance that runs the application. This couples the application and the database, so a failure of that instance takes both down. It also leaves the team responsible for patching, backups, and scaling the database. The business needs a managed, isolated database tier that can be created repeatably and monitored, without losing any existing order data and with minimal change to the application.
## Objectives
	- Create an Amazon RDS MariaDB instance by using the AWS CLI.
	- Migrate data from a MariaDB database on an EC2 instance to an Amazon RDS MariaDB instance.
# Architecture Diagram
## Initial Architecture Diagram

![unknown_asset](<architecture-diagram/architecture-diagram-before.png>)

## Final Architecture Diagram

![unknown_asset](<architecture-diagram/architecture-diagram-after.png>)

# Scope and Limitation
	- Due to restrictions in the lab environment, some services were already provisioned by AWS: the VPC and its public subnet, the CafeInstance (web server with the local MariaDB), the CLI Host instance, the CafeSecurityGroup, the Parameter Store entries, and the AWS credentials/permissions. Access Keys and Secret Keys were given instead of an IAM role for the EC2 instances. The laboratory is simply focus on exploring one of the many different ways to migrate a data. This is not the best practice but enough to give context for beginners.
# Implementation
## STEP 1: Generating an order data on the cafe website
1. Search for *EC2* in AWS Management Console.

![unknown_asset](<assets/Pasted image 20261020125544.png>)

2. At the navigation pane, select *Instances* and tick the *CafeInstance*. It will show its details at the main window. Copy the *Public IPv4 address*.
3. To access the website, go to any browser and search for `http://<ipv4 ip address>/cafe`
4. Interact with the website and submit an order to create a transaction history data for the database. **Note:** Remember the total.

![unknown_asset](<assets/Pasted image 20261020125818.png>)

## STEP 2: Creating an Amazon RDS instance by using the AWS CLI
### STEP 2.1: Connecting to the CLI Host Instance
1. Still in *EC2 Instances*, tick the *CLI Host* and choose *Connect*.

![unknown_asset](<assets/Pasted image 20261020131618.png>)

2. Choose the *EC2 Instance Connect*.

![unknown_asset](<assets/Pasted image 20261020131644.png>)

### STEP 2.2: Configuring AWS CLI
1. Configure the *EC2 Instance Connect* with the following:
	- **AWS Access Key:** `<insert access key>`
	- **Secret Key:** `<insert secret key>`
	- **Region:** `us-west-2`
	- **Output:** `json`

```Bash
aws configure
```

### STEP 2.3: Creating prerequisite components
#### STEP 2.3.1: Creating CafeDatabaseSG (Security Group)
1. Get the Instance ID for the CafeInstance provisioned by AWS. Take note of the output.

```Bash
aws ec2 describe-instances \
    --filters "Name=tag:Name,Values=<instance-name>" \
    --query "Reservations[*].Instances[*].InstanceId" \
    --output text
```

2. Get the VPC ID where the CafeInstance reside. Use the Instance ID obtained from the previous step. Take note of the output of the query.

```Bash
aws ec2 describe-instances \
    --instance-ids i-xxxxxxxxxxxxxxxxx \
    --query "Reservations[*].Instances[*].VpcId" \
    --output text
```

3. Create the CafeDatabaseSG within the same VPC of the CafeInstance. Take note of the Group ID output. This would be used in the succeeding steps.

```Bash
aws ec2 create-security-group \
	--group-name CafeDatabaseSG \
	--description "Security group for Cafe database" \
	--vpc-id <CafeInstanceVPCId> 
```

4. To create the inbound rule, run the following command. In the command, replace `<CafeDatabaseSG Group ID>` with the **GroupId** value that you recorded in the previous step, and replace `<CafeSecurityGroup Group ID>` with the **CafeSecurityGroupID**:

```Bash
aws ec2 authorize-security-group-ingress \
	--group-id <CafeDatabaseSG Group ID> \
	--protocol tcp --port 3306 \
	--source-group <CafeSecurityGroup Group ID>
```

5. To confirm that the inbound rule was applied appropriately, run the following command:

```Bash
aws ec2 describe-security-groups \
	--query "SecurityGroups[*].[GroupName,GroupId,IpPermissions]" \
	--filters "Name=group-name,Values='CafeDatabaseSG'"
```

#### STEP 2.3.2: Create CafeDB Private Subnet 1
1. To create a Private Subnet, run the following command. The given CIDR block allows for **507 Usable IPs**.

```Bash
aws ec2 create-subnet \
	--vpc-id  <CafeInstance VPC ID> \
	--cidr-block 10.200.2.0/23 \
	--availability-zone us-west-2a
```

2. Take note of the *Subnet ID*. to be used later.
#### STEP 2.3.3: Create a CafeDB Private Subnet 2
1. To create a Private Subnet, run the following command. The given CIDR block allows for **507 Usable IPs**. It is important that the Availability Zone for Private Subnet 2 is different from the Private Subnet 1.

```Bash
aws ec2 create-subnet \
	--vpc-id  <CafeInstance VPC ID> \
	--cidr-block 10.200.4.0/23 \
	--availability-zone us-west-2b
```

2. Take note of the *Subnet ID*, to be used later
	**Note:** Based on the configuration of AWS Route Table, the private route table is not explicitly applied to it but it is the main route table. For a more secure setup, explicitly associate it to the private subnets.

#### STEP 2.3.4: CafeDB Subnet Group
1. Run the command to create a subnet group consisting of CafeDB Private Subnet 1 and 2. Add the `CafeDB Private Subnet 1` and `CafeDB Private Subnet 2` obtained from **STEP 2.3.2 and STEP 2.3.3**.

```Bash
aws rds create-db-subnet-group \
	--db-subnet-group-name "CafeDB Subnet Group" \
	--db-subnet-group-description "DB subnet group for Cafe" \
	--subnet-ids <Cafe Private Subnet 1 ID> <Cafe Private Subnet 2 ID> \
	--tags "Key=Name,Value=CafeDatabaseSubnetGroup"
```

### STEP 2.4: Creating the Amazon RDS MariaDB instance
	Create an Amazon RDS MariaDB instance with the following configuration settings:

	- DB instance identifier: CafeDBInstance
	- Engine option: MariaDB
	- DB engine version: 10.11
	- DB instance class: db.t3.micro
	- Allocated storage: 20 GB
	- Availability Zone: CafeInstanceAZ
	- DB Subnet group: CafeDB Subnet Group
	- VPC security groups: CafeDatabaseSG
	- Public accessibility: No

1. To create the Amazon RDS MariaDB Instance based on the requirements set by AWS, run the command below. The MariaDB Instance was deployed to us-west-2a as per the architecture diagram.

```Bash
aws rds create-db-instance \
	--db-instance-identifier CafeDBInstance \
	--engine mariadb \
	--engine-version 10.11 \
	--db-instance-class db.t3.micro \
	--allocated-storage 20 \
	--availability-zone us-west-2a \
	--db-subnet-group-name "CafeDB Subnet Group" \
	--vpc-security-group-ids <CafeDatabaseSG Group ID> \
	--no-publicly-accessible \
	--master-username root --master-user-password <'insert password here'>
```

2. Wait for the CafeDBInstance to become **available**. Run the following command to monitor its status.

```Bash
aws rds describe-db-instances \
	--db-instance-identifier CafeDBInstance \
	--query "DBInstances[*].[Endpoint.Address,AvailabilityZone,PreferredBackupWindow,BackupRetentionPeriod,DBInstanceStatus]"
```

3. Once *available*, copy and save the *Endpoint address* for later use.
## STEP 3: Migrating application data to Amazon RDS instance
1. Go to the AWS Management Console under *EC2 Instances*. Connect to the *CafeInstance*.
2. Select the *EC2 Instance Connect*.
3. Setup the *CafeInstance* AWS CLI similar with the configuration in **STEP 2.2**.
4. Use *mysqldump* utility that was already provisioned by AWS to create a backup file of the Cafe DB inside the *EC2 Instance*. 

```Bash
mysqldump --user=root --password=<'insert password here'> \
	--add-drop-database --databases cafe_db > cafedb-backup.sql
```

	This command generates SQL statements in a file named cafedb-backup.sql, which can be run to reproduce the schema and data of the original cafe_db database.
5. To verify that mysqldump is successful, use `ls` or `less cafedb-backup.sql` for a more comprehensive approach.
6. The Amazon RDS MariaDB instance requires encrypted (SSL/TLS) connections by default. Before connecting, you must download the Amazon RDS Certificate Authority (CA) bundle. To obtain an RDS CA, run the following command.

```Bash
curl -o global-bundle.pem https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
```

7. Once CA is obtained, import the database backup file to the MariaDB Instance

```Bash
mysql --user=root --password=<'insert password here'> \
--host=<RDS Instance Database Endpoint Address> \
--ssl-ca=./global-bundle.pem \
< cafedb-backup.sql
```

8.  To observe if the database was successfully migrated to the MariaDB Instance, run the command to connect with the MariaDB Instance.

```Bash
mysql --user=root --password=<'insert password here'> \
	--host=<RDS Instance Database Endpoint Address> \
	--ssl-ca=./global-bundle.pem \
	cafe_db
```

9. Once connection has been established, run the following commands.

```MySQL
SELECT * FROM cafe_db.product;
```

	The command above would show all the products being sold in the Cafe Website along with their prices.

```MySQL
SELECT * FROM cafe_db.order;
```

	The tables contains the order transactions created by the user inside the Cafe Website. It should have 1 row of data that has similar total amount with the transaction performed in STEP 1.
## STEP 4: Configuring the website to use the Amazon RDS instance
1. In the AWS Management Console, search for systems manager.

![unknown_asset](<assets/Pasted image 20261020140719.png>)

2. At *systems manager*, go to *Parameter Store* found at the navigation pane.
3. Tick the `/cafe/dbURL` and select *Edit*. 
4. Under the *Parameter*, scroll down to *Value*. Change the value with the RDS Instance Database Endpoint and **Save**.
## STEP 5: Monitoring the Amazon RDS database
1. Simulate a transaction to the Cafe Website by submitting another order. Take note of the total as this would be monitored later.

![unknown_asset](<assets/Pasted image 20261020141159.png>)

2. Connect to the *CafeInstance* via *EC2 Instance Connect*. 
3. Repeat the **STEP 3: Number 8** to establish a connection to the *RDS database*. 
4. Once connected, run the same commands found at **STEP 3: Number 9**.

![unknown_asset](<assets/Pasted image 20261020141600.png>)

	Note that the total for the second row is 20.50 which is equal to the order submitted at STEP 5: Number 1. This implies that database for the Cafe Instance website has been successfully transferred to a MariaDB Instance.
# Lessons Learned
- A newly created **subnet** without any explicit associations to any routing tables, would be  **implicitly associated** to all the exiting routing tables formed in the **VPC**. The **Main** routing table would be automatically linked to it.
- **AWS Parameter Store** allows edit of configuration settings without downtime, redeployment, and safer operations.