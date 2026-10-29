# Project Title and Summary
## Title: Implementing DNS Failover Routing with Amazon Route 53 Health Checks
## Project Summary
	- This project sets up DNS failover for a cafe website hosted on two Amazon EC2 instances in different Availability Zones. A Route 53 health check monitors the primary website, and a CloudWatch alarm with an Amazon SNS topic sends an email when the primary becomes unhealthy. Failover routing records in an existing hosted zone redirect traffic to the secondary website automatically. The setup was tested by stopping the primary instance and confirming that the site was served from the secondary Availability Zone.
## Tech/Skill Used
- **Amazon Route 53:** Health checks, hosted zones, and failover routing records.
- **Amazon CloudWatch:** Alarm based on the health check percentage metric.
- **Amazon SNS:** E-mail notifications for unhealthy endpoints.
- **Amazon EC2:** Hosts the cafe website (LAMP stack) in two Availability Zones.
- **DNS:** Record types, TTL, and failover resolution.
# Problem Statement and Objectives
## Problem Statement
	- A website running on a single server is a single point of failure. If the server or its Availability Zone becomes unavailable, users can no longer reach the site, and nobody is notified unless the problem is detected. The cafe website is deployed on two EC2 instances in separate Availability Zones, but DNS has no way of knowing when the primary instance is down, so traffic keeps going to the failed endpoint. This project addresses that by monitoring the health of the primary website and automatically routing traffic to the secondary website when the primary fails.
## Objectives
	- Configure a Route 53 health check that sends emails when the health of an HTTP endpoint becomes unhealthy.
	- Implement a failover routing in Route 53.
# Architecture Diagram

![unknown_asset](<architecture-diagram/architecture-diagram.png>)

# Scope and Limitation
	- Project focuses on implementation of failover routing to an existing Amazon Route 53 Hosted Zone. AWS has provisioned two existing Amazon EC2 instances where each has the full LAMP stack installed and a cafe website deployed and running in two different Availability Zones (us-west-2a and us-west-2b). Additionally, the networking aspect is already configured.
# Implementation
## Step 1: Confirming the cafe websites
1. Obtain the two *Public IP Addresses* of the EC2 instance provisioned by AWS.
2. On any browser, test both IP address. It should look like this `http://<ip-address>/cafe`.

![unknown_asset](<assets/Pasted image 20261015163323.png>)

![unknown_asset](<assets/Pasted image 20261015163403.png>)

## Step 2: Configure a Route 53 health check
1. In AWS Management Console, search for *Route 53*.

![unknown_asset](<assets/Pasted image 20261015171026.png>)

2. At the left pane, select *Health checks*. Choose *Create health check* at the upper right of the main window.

![unknown_asset](<assets/Pasted image 20261015171037.png>)

3. Configure the health check by implementing the following:
	- **Name:** `Primary-Website-Health`
	- **Resource:** Select *Endpoint*.
	- **Specified endpoint by:** Select IP addresses.
	- **HTTP:** `<primary-ip-address/cafe>`

![unknown_asset](<assets/Pasted image 20261015171104.png>)

4. Under *request interval*, select *Fast (10 seconds)* and a *Failure threshold* `2`.

![unknown_asset](<assets/Pasted image 20261015171121.png>)

5. Create the health check.
6. Under the details of the health check, select *Alarms* at the menu and *Create a CloudWatch alarm*. A dropdown will appear and choose the *Health Check Percentage*.

![unknown_asset](<assets/Pasted image 20261015171138.png>)

7. In the new tab, select the following configuration:
	- **Data source:** Tick *Metrics*
	- **Type:** Choose *Classic*

![unknown_asset](<assets/Pasted image 20261015171155.png>)

8. Under *Metric*, change the following:
	- **Period:** 1 minute

![unknown_asset](<assets/Pasted image 20261015171223.png>)

9. Under *Conditions*, select the following:
	- **Threshold type:** Static
	- **Whenever HealthCheckPercentageHealthy is..:** Lower/Equal
	- **than...:** `90`

![unknown_asset](<assets/Pasted image 20261015171238.png>)

9. At the next step, configure the notifications. Click on *Add notification*.

![unknown_asset](<assets/Pasted image 20261015171257.png>)

9. Construct the notification with the following setup:
	- **Alarm state trigger:** *In alarm*
	- **Send a notification to the following SNS topic:** Choose *Create new topic*
	- *Create a new topic...:* `Primary-Website-Health`
	- **Email endpoints that will receive the notification...:** `inset-email-here`

![unknown_asset](<assets/Pasted image 20261015171432.png>)

9. Skip to *Preview and create*. Review the configuration before creating the health check.
## Step 3: Configuring Route 53 record
1. At the same **Route 53 Console**, select *Hosted zones*, By default, AWS has provisioned a hosted zone.

![unknown_asset](<assets/Pasted image 20261015171514.png>)

2. Select the zone given and choose the *Create record* button at the main window.

![unknown_asset](<assets/Pasted image 20261015172124.png>)

### Step 3.1: Creating a record for the primary website
- **Record name:** `www`
- **Record type:** `A - Routes traffic to an IPv4 address and some AWS resources.`
- **Value:** `<primary-ip-address>`
- **TTL:** `15`
- **Failover record type:** `Failover`
- **Health check ID:** select *Primary-Website-Health*
- **Record ID:** `FailoverPrimary`
### Step 3.2: Create a record for the secondary website
- **Record name:** `www`
- **Record type:** `A - Routes traffic to an IPv4 address and some AWS resources.`
- **Value:** `<primary-ip-address>`
- **TTL:** `15`
- **Failover record type:** `Failover`
- **Health check ID:** leave blank
- **Record ID:** `FailoverSecondary`
## Step 4: Verifying DNS resolution
1. Under *Records*, look at the *Record name* column and copy the *Record name* of the *Primary*.

![unknown_asset](<assets/Pasted image 20261015172616.png>)

2. Paste the *Record name* with `/cafe`. It should look like this `http://<primary-record-name/cafe`.

![unknown_asset](<assets/Pasted image 20261015172709.png>)

## Step 5: Verifying the failover functionality
1. To simulate failover, search for *EC2* in the AWS Management Console.

![unknown_asset](<assets/Pasted image 20261015172825.png>)

2. At the left pane, select *Instances* and tick the *Primary Instance*.

![unknown_asset](<assets/Pasted image 20261015173040.png>)

3. Select the *Instance state* and choose *Stop instance*.

![unknown_asset](<assets/Pasted image 20261015173133.png>)

4. In *Route 53 Console*, select *Health Checks* and observe the *Health Check* created at **Step 2**.
5. Wait until the monitor for *Health checkers that report the endpoint health (percent)* changes and becomes unhealthy.
	**Optional:** An alternative is to monitor the status in the *Alarm* section.

![unknown_asset](<assets/Pasted image 20261015173731.png>)

6. Once it is unhealthy, refresh the webpage and observe the Availability Zone which changed from *us-west-2a* to *us-west-2b*.

![unknown_asset](<assets/Pasted image 20261015173835.png>)

# Lessons Learned
- Amazon Route 53 operates as a global service; however, it publishes all health check metrics exclusively to the **US East (N. Virginia) (us-east-1)** region. Consequently, both the **Amazon CloudWatch alarm** and its corresponding **Amazon SNS topic** must be provisioned in *us-east-1* to ensure successful metric evaluation and notification delivery.