# Project Title and Summary
## Title: Highly Available and Auto-Scaling Web Application on AWS Using an Application Load Balancer and EC2 Auto Scaling Group
## Project Summary
	- This project deploys a highly available and elastic web application on AWS. An internet-facing Application Load Balancer distributes incoming traffic across EC2 instances in an Auto Scaling Group. The group launches from a custom AMI and a launch template, and sits in private subnets across two Availability Zones. A target tracking policy adds or removes instances based on average CPU utilization. A load test provided by AWS drove CPU usage up, and the Auto Scaling group scaled out in response, as observed through CloudWatch alarms.
## Tech/Skill Used
- **Amazon EC2:** Hosts the web application on t3.micro instances.
- **Amazon Machine Image (AMI):** Captures the configured website instance as a reusable template. 
- **EC2 Launch Template:** Defines the AMI, instance type, and security group for every new instance. 
- **EC2 Auto Scaling Group:** Maintains between two and four instances and replaces unhealthy ones automatically. 	- **Target Tracking Scaling Policy:** Scales the group automatically to keep average CPU utilization near 50%. 
- **Application Load Balancer:** Distributes HTTP traffic across instances in multiple Availability Zones.  	
- **Target Groups and Health Checks:** Route traffic only to healthy instances.
- **Amazon VPC (public and private subnets):** Keeps instances isolated while only the load balancer is internet-facing. 
- **Amazon CloudWatch:** Monitors CPU utilization and the alarms that trigger scaling. 
- **Load Testing:** Validates scaling behavior under high CPU load.
# Problem Statement and Objectives
## Problem Statement
	- A web application running on a single EC2 instance has a single point of failure. If the instance or its Availability Zone fails, the website goes down. A fixed number of instances also cannot adapt to changing demand. During traffic spikes, high CPU load slows responses or makes the site unavailable. Provisioning extra instances by hand is slow and error-prone, and keeping extra capacity running all the time wastes money during quiet periods. The application needs a setup that distributes traffic across multiple instances in different Availability Zones, replaces unhealthy instances automatically, and adds or removes capacity based on demand.
## Objectives
	- Deploy an internet-facing Application Load Balancer that distributes incoming traffic to the instances of the Auto Scaling Group across two Availability Zones. 
	- Deploy an Auto Scaling Group with a minimum and desired capacity of two EC2 instances and a maximum of four, scaling on average CPU utilization with a target of 50%. 
	- Verify the Auto Scaling policy by running the AWS-provided load test and monitoring the resulting scaling activity in CloudWatch.
# Architecture Diagram

## Initial Architecture Diagram

![unknown_asset](<architecture-diagram/architecture-diagram-before.png>)

## Final Architecture Diagram

![unknown_asset](<architecture-diagram/architecture-diagram-after.png>)

# Scope and Limitaton
	- An EC2 instance that will serve as the AMI template, is already provisioned by AWS along with the website data. All networking aspect of the project is already provisioned due to prior laboratories with networking to eliminate redundancy and long configuration. This project focuses on utilizing AWS Auto Scaling Group deployment via console.
# Implementation
## Step 1: Create an AMI for auto scaling
1. Search for *EC2* in AWS Management Console.

![unknown_asset](<assets/Pasted image 20261014232800.png>)

2. In the left pane, locate *Instances*.

![unknown_asset](<assets/Pasted image 20261014232819.png>)

3. Tick the instance provisioned by AWS. Click on *Actions > Image and templates > Create image*.
	**Note:** This instance contains the website data to be used for testing.

![unknown_asset](<assets/Pasted image 20261014232907.png>)

![unknown_asset](<assets/Pasted image 20261014232927.png>)

## Step 2: Create a load balancer
1. Scroll down to *Load Balancing* and select *Load Balancer*. Click on the *Create load balancer* button.

![unknown_asset](<assets/Pasted image 20261014232947.png>)

2. Select *Application Load Balancer*.

![unknown_asset](<assets/Pasted image 20261014232957.png>)

3. Under *Basic configuration*, configure the following:
	- **Load balancer name:** `<balancer-name>`
	- **Scheme:** Internet-facing

![unknown_asset](<assets/Pasted image 20261014233345.png>)

4. Under *Network mapping,* select the **VPC** configured by AWS. For *Availability Zone and subnets* choose the two public subnets in different AZs.
	Selecting public subnets for the load balancer enables accepting packets from two different AZs for high availability.

![unknown_asset](<assets/Pasted image 20261014233357.png>)

5. Under *Default action,* select *Forward to target groups* and create a *target group*. Another tab will appear.

![unknown_asset](<assets/Pasted image 20261014233411.png>)

6. In create target group, choose *Instances* since the focus is to create an auto scaling group. Create a *Target group name.*

![unknown_asset](<assets/Pasted image 20261014233453.png>)

7. Under *VPC*, select the given AWS VPC. After that, skip all other steps then hit create.

![unknown_asset](<assets/Pasted image 20261014233615.png>)

8. Finish the setup for the Load Balancer.
## Step 3: Create a launch template
1. In *EC2 Services,* select *Launch Templates*.

![unknown_asset](<assets/Pasted image 20261014233648.png>)

2. Add a *Launch template name* and *Template version description.* Additionally, tick the *Provide guidance to help me set up a template that I can use with EC2 Auto Scaling.*

![unknown_asset](<assets/Pasted image 20261014233749.png>)

3. Under *Launch template contents*, select *My AMIs* to use the AMI created at **Step 1**.

![unknown_asset](<assets/Pasted image 20261014233843.png>)

4. Under *Instance type*, choose *t3.micro*. Key pair is not needed for this project.

![unknown_asset](<assets/Pasted image 20261014233857.png>)

5. Under *Network settings,*  Do not include subnet in the launch template and for security group, choose the provisioned security group.

![unknown_asset](<assets/Pasted image 20261014233931.png>)

6. Create the launch template.
## Step 4: Create an Auto Scaling Group
1. Still under *EC2 services,* scroll down to select *Auto Scaling Groups* and click on *Create Auto Scaling group*.

![unknown_asset](<assets/Pasted image 20261014234020.png>)

2. Under *Choose launch template or configuration*, add an *Auto Scaling group name* and choose the *Launch template* created at **Step 3**.

![unknown_asset](<assets/Pasted image 20261014234037.png>)

3. Under *Choose instance launch options*, select the VPC provisioned and choose the two private subnets.
	Selecting the private subnets assigns those subnets to the EC2 instance that will be provisioned via Auto Scaling Groups. This makes it more secure since only load balancer is front facing while the EC2 instances are isolated.

![unknown_asset](<assets/Pasted image 20261014234143.png>)

4. Under *Integrate with other services,* attach the Auto Scaling group to the existing load balancer deployed at **Step 2**. Select *Choose from your load balancer target groups* and find the target group also created at **Step 2**.

![unknown_asset](<assets/Pasted image 20261014234208.png>)

5. For *Health checks*, tick the *Turn on Elastic Load Balancing health checks*.

![unknown_asset](<assets/Pasted image 20261014234222.png>)

6. Under *Configure group size and scaling*, configure the following:
	- **Desired capacity:** `2`
	- **Min desired capacity:** `2`
	- **Max desired capacity:** `4`
	- **Automatic scaling:** Target tracking scaling policy
	- **Metric type:** `Average CPU utilization`
	- **Target value:** `50`

![unknown_asset](<assets/Pasted image 20261014234237.png>)

![unknown_asset](<assets/Pasted image 20261014234249.png>)

7. Skip *Add notifications*. For *Tags*, set the following:
	- **Key:** `Name`
	- **Value:** `Lab Instance`

![unknown_asset](<assets/Pasted image 20261014234317.png>)

7. Review and create the Auto Scaling group.
## Step 5: Verify load balancer
1. Under *EC2 services*, select *Target Groups* then tick the created target group. 
2.  Under its *Registered targets* it should have two lab instances and wait for the status to change to *healthy*.
## Step 5: Test auto scaling
1. In the left pane, select the *Load Balancers* and tick the deployed Elastic Load Balancer. Under its details, scroll down and copy the *DNS name*. 

![unknown_asset](<assets/Pasted image 20261014234626.png>)

2. Using any browser, paste the DNS name but use http instead of https.
3. Try to reload the website a few times to verify that the *Availability Zone* and *InstanceId* changes.

![unknown_asset](<assets/Pasted image 20261014234716.png>)

![unknown_asset](<assets/Pasted image 20261014234736.png>)

4. Click on the *Load Test* to increase the *Current CPU Load*. 
5. Go back to the console and search for *CloudWatch*. This helps in monitoring the *Average CPU utilization* used in *Target tracking scaling policy* of Auto Scaling group.

![unknown_asset](<assets/Pasted image 20261014234803.png>)

4. Select *Alarms*.
	Choose the alarm that has **AlarmHigh** in its name. This alarm should have a **State** of *OK*.

	If the alarm is not showing  *OK* for the **State**, wait a minute and then choose refresh until the **State** changes.

	The *OK* state indicates that the alarm has not been initiated. It is the alarm for **CPU Utilization > 50**, which adds instances when the average CPU utilization is high. The chart should show very low levels of CPU at the moment.

![unknown_asset](<assets/Pasted image 20261014234913.png>)

5. Wait until the **AlarmHigh** alarm enters the *In alarm* state. Once in that state, observe the number of EC2 instances provisioned by the Auto Scaling group. 
	Since detailed monitoring is disabled, it may take up to  5 minutes before the state changes in the CloudWatch.

![unknown_asset](<assets/Pasted image 20261014234950.png>)

![unknown_asset](<assets/Pasted image 20261014235015.png>)

**Optional:** Wait until the load test finished and observe how the Auto Scaling group downsizes.
# Lessons Learned
- AMI and launch template allow uniformity across multiple EC2 instances.
- Only the load balancer should be exposed to the internet via public subnets while EC2 instance are in private subnets to reduce its exposure and threats.
- Scaling works in both ways. When a CPU utilization triggers **AlarmLow**, any excess EC2 instances are terminated.
- Simply reloading a website can trigger load balancing.
- CloudWatch detailed monitoring is disabled by default which makes the detection of an increase or decrease in CPU utilization would take quite a while to reflect in the alarm status.

