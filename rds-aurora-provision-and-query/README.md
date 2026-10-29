# Build Your DB Server and Interact With Your DB

# Background
	This lab is designed to reinforce the concept of leveraging an AWS-managed database instance for solving relational database needs.
# Objectives
	- Launch an RDS instance that uses Amazon Aurora (MySQL Compatible).
	- Establish an SSH connection with EC2 Instance.
	- Interact with the RDS via EC2.
# Scope and Limitation
	An EC2 Instance and VPC has been provisioned in this laboratory to shift the focus on generation and interaction with the database.
# SQL Challenges
1. Create a table RESTART with the following columns (with 10 rows)
	- Student ID (Number)
	- Student Name
	- Restart City
	- Graduation Date (Date Time)
2. Create a table CLOUD_PRACTITIONER with the following columns (with 5 rows)
	- Student ID (Number)
	- certification date (Date Time)
3. Perform an inner join between the 2 tables created above and display student ID, Student Name, Certification Date
# AWS Architecture

![unknown_asset](<architecture-diagram/architecture-diagram.png>)

# Methodology
## Step 1: Configure Relational Database Service
1. Use the AWS Management Console search bar to locate *RDS*.

![unknown_asset](<assets/Pasted image 20260922165406.png>)

2. In the left navigation pane, choose *Databases*.

![unknown_asset](<assets/Pasted image 20260922165549.png>)

3. In workspace, choose *Create database*. Drop down menu will appear, select *Full Configuration*.

![unknown_asset](<assets/Pasted image 20260922165724.png>)

![unknown_asset](<assets/Pasted image 20260922165840.png>)

4. Choose an engine option, use *Aurora (MySQL Compatible)*. Select ***Full Configuration*** as the creation method.

![unknown_asset](<assets/Pasted image 20260922170013.png>)

5. In **Templates**, choose *Dev/Test* and under **Cluster Scalability Type** select *Provisioned*. Then use  *Burstable Classes and db.t3.medium* as the instance class.

![unknown_asset](<assets/Pasted image 20260922170318.png>)

6. Name the **DB cluster identifier** to *testdb*.

![unknown_asset](<assets/Pasted image 20260922170825.png>)

7. Under **Credentials Management**, use *Self managed* to assign a master password.

![unknown_asset](<assets/Pasted image 20260923173504.png>)

8. For **Connectivity**, assign a VPC, DB Subnet Group, and Security Group.

![unknown_asset](<assets/Pasted image 20260922171811.png>)

![unknown_asset](<assets/Pasted image 20260922171909.png>)

9. Uncheck *Enable Enhanced Monitoring*.

![unknown_asset](<assets/Pasted image 20260922172124.png>)

10. Assign *Initial database name* under **Additional Configuration**.

![unknown_asset](<assets/Pasted image 20260922172302.png>)

11. Wait for the **status** to become **Available**. Take note of the *write endpoint* of your cluster

![unknown_asset](<assets/Pasted image 20260922174740.png>)

## Step 2: Reconfigure Security Group
1. Use the AWS Management Console search bar to locate *VPC*.

![unknown_asset](<assets/Pasted image 20260922172501.png>)

2. In your left navigation pane, choose *Security groups*.

![unknown_asset](<assets/Pasted image 20260922172526.png>)

3. In workspace, find the security group assigned to the RDS. Choose *Edit inbound rule* to add *MySQL/Aurora* as the type and assign the *same security group* as the source

![unknown_asset](<assets/Pasted image 20260922173227.png>)

![unknown_asset](<assets/Pasted image 20260922173330.png>)

## Step 3: Connect to EC2 Instance via SSH
1. Find the EC2 instance deployed and copy its *Public IPv4 address*

![unknown_asset](<assets/Pasted image 20260922173749.png>)

2. Connect via SSH with your .pem or .ppk key file

![unknown_asset](<assets/Pasted image 20260922174025.png>)

## Step 4: Interact with the RDS via EC2
1. Before accessing RDS, install MariaDB inside the EC2 instance

```Bash
sudo yum install mariadb -y
```

2. To connect in RDS, input the following:

```Bash
mysql -u admin --password=<password goes here> -h <endpoint goes here>
```

3. Verify the databases

![unknown_asset](<assets/Pasted image 20260922175005.png>)

4. For Challenge 1: Create a table *RESTART* with the following columns (with 10 rows)
	- Student ID (Number)
	- Student Name
	- Restart City
	- Graduation Date (Date Time)

```MySQL
CREATE TABLE restart(
	student_id INT PRIMARY KEY,
	student_name VARCHAR(255) NOT NULL,
	restart_city VARCHAR(255) NOT NULL,
	graduation_date TIMESTAMP NOT NULL
);

INSERT INTO restart (student_id, student_name, restart_city, graduation_date) 
VALUES	
(101, 'Renato Bautista', 'Quezon City', '2026-10-30 10:00:00'),
(102, 'Elena Dimaculangan', 'Manila', '2026-06-15 14:30:00'),
(103, 'Manuel Macaraeg', 'Caloocan', '2026-10-24 09:00:00'),
(104, 'Christina Alcantara', 'Pasig', '2026-03-20 11:15:00'),
(105, 'Ferdinand Soriano', 'Taguig', '2026-06-15 10:00:00'),
(106, 'Grace Villanueva', 'Makati', '2026-12-18 16:00:00'),
(107, 'Ricardo Dizon', 'Las Piñas', '2026-06-16 08:30:00'),
(108, 'Patricia Mendoza', 'Parañaque', '2026-05-30 13:00:00'),
(109, 'Eduardo De Leon', 'Mandaluyong', '2026-01-10 15:45:00'),
(110, 'Teresa Mercado', 'Marikina', '2026-06-15 10:00:00');
```

![unknown_asset](<assets/Pasted image 20260922180209.png>)

5. For Challenge 2: Create a table *CLOUD_PRACTITIONER* with the following columns (with 5 rows)
	- Student ID (Number)
	- certification date (Date Time)

```MySQL
CREATE TABLE cloud_practitioner(
	student_id INT PRIMARY KEY,
	certification_date TIMESTAMP NOT NULL,
);

INSERT INTO cloud_practitioner (student_id, certification_date)
VALUES
(101, '2026-11-05 09:30:00'),
(104, '2026-04-12 14:00:00'),
(110, '2026-07-01 10:15:00'),
(111, '2026-08-24 11:00:00'),
(112, '2026-09-15 15:45:00');
```

![unknown_asset](<assets/Pasted image 20260922180238.png>)

6. For Challenge 3: Perform an inner join between the 2 tables created above and display student ID, Student Name, Certification Date

```MySQL
SELECT r.student_id, r.student_name, cp.certification_date
FROM restart r
INNER JOIN cloud_practitioner cp
USING (student_id);
```

![unknown_asset](<assets/Pasted image 20260923181456.png>)

# Lessons Learned
* **Storage Layer:** Amazon Aurora automatically mirrors data **6 ways across 3 Availability Zones**. While this distributed storage fabric lives on an isolated AWS storage tier (consuming no VPC IP addresses), the 3 Availability Zones it uses are **directly determined by the AZs configured in your VPC's DB Subnet Group**.
* **Compute Layer:** An Aurora cluster consists of **1 Primary Writer instance and up to 15 Reader instances.** These compute instances are provisioned directly inside your VPC, specifically deployed into a **DB Subnet Group**, which is simply a collection of your pre-existing VPC subnets spanning at least two or three Availability Zones.
* With the setup created, it is important to take note that the **security group must explicitly allow Inbound Rules for MySQL/Aurora** to establish a communication between the EC2 Instance and database.