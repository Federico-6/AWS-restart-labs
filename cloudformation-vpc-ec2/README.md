# Project Title and Summary
## Title: Deploying a VPC and Private EC2 Instance Using AWS CloudFormation
## Project Summary
	- This project uses AWS CloudFormation to deploy a basic network environment as Infrastructure as Code (IaC). A single YAML template provisions a Virtual Private Cloud (VPC), an internet gateway attached to it, a private subnet, a security group that allows SSH (port 22), and a t3.micro EC2 instance running the latest Amazon Linux 2023 in the private subnet. Parameters keep the CIDR ranges and AMI ID configurable, so the stack can be redeployed consistently without manual console clicks.
## Tech/Skill Used
	- **AWS CloudFormation:** stacks, templates, parameters, resources, `!Ref`
	- **Amazon VPC:** VPC, subnets, internet gateway, default route table
	- **Amazon EC2:** t3.micro instance, security groups
	- **AWS Systems Manager Parameter Store:** dynamic AMI lookup
	- **YAML:** writing and structuring templates
	- **Skills:** Infrastructure as Code, cloud networking fundamentals, resource dependency handling
# Problem Statement and Objectives
## Problem Statement
	- Creating cloud networking and compute resources manually in the AWS Management Console is slow, hard to repeat, and prone to misconfiguration. It also leaves no record of how an environment was built. A reusable template is needed so the same VPC and EC2 setup can be deployed, reviewed, and removed consistently.
## Objectives
	- Write a CloudFormation template in YAML that defines the full environment.
	- Use parameters for the VPC CIDR, subnet CIDR, and AMI ID instead of hard-coding them.
	- Deploy a VPC with an attached internet gateway and a private subnet.
	- Create a security group allowing inbound SSH (port 22).
	- Launch a t3.micro EC2 instance inside the private subnet.
	- Deploy the template as a stack through the CloudFormation console.
	- Understand how `!Ref` creates implicit dependencies between resources.
# Architecture Diagram

![unknown_asset](<architecture-diagram/architecture-diagram.png>)

# Scope and Limitation
	- The project focuses on creating a CloudFormation stack to deploy a Virtual Private Cloud (VPC), internet gateway (IGW), security group that allows ingress of SSH (Port 22) to the public, a private subnet, and an EC2 instance. The EC2 instance is required to use t3.micro and within the private subnet. It is not necessary to access the EC2 instance via SSH based on the configuration given by AWS.
# Implementation
## STEP 1: Create a CloudFormation template
1. Create a yaml file to create a template. You may opt for a json file but for this project, I strictly used a yaml file to deploy the setup. The template is accessible below but block-by-block guide is provided.
	- **Template:** [main.yaml](templates/main.yaml)
2.  Write the *top-level sections*.

```YAML
AWSTemplateFormatVersion: 2010-09-09
Description: VPC and EC2 template
```

- **AWSTemplateFormatVersion:** Represents the format version of the AWS CloudFormation template.
- **Description:** An **optional** property that describes what the template does.

### Parameter Block
	- An optional block in AWS CloudFormation template that allows you to pass custom input values into your template. It is similar to how variables work. The AmazonLinuxAmiId is a parameter that fetches the latest Amazon Linux 2023 in the Parameter Store of Systems Manager.

```YAML
Parameters:
  VpcCidr:
    Type: String
    Default: 10.0.0.0/16
  
  PrivateSubnetCidr:
    Type: String
    Default: 10.0.0.0/24

  AmazonLinuxAmiId:
    Type: AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>
    Default: /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64
```

### Resources Block
	- It is the only mandatory block in AWS CloudFormation template. It defined the actual AWS infrastructure components that the CloudFormation will create, configure, deploy and manage. The main parts of a resource are the following:

- **Logical ID:** A unique alphanumeric name assign to different components for referencing. (e.g. LabVpc and LabIgw)
- **Type:** The official AWS resource type identifier.
- **Properties:** Specific configurations and settings for individual components. May be required or optional.
#### VPC & Core Networking
	- The following block creates the VPC, the Internet Gateway, and attached the Internet Gateway to the VPC. Using !Ref tells the AWS CloudFormation that you are about to use a parameter. This automatically makes the CloudFormation to wait for the provisioning of the said parameter/s before the execution of that block. In this case, the "VpcGatewayAttachment".

```YAML
Resources:

##############################
# VPC & Core Networking
##############################

  LabVpc:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: !Ref VpcCidr
      EnableDnsSupport: true
      EnableDnsHostnames: true
      Tags:
        - Key: Name
          Value: Lab VPC

  LabIgw:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: Lab IGW

  VpcGatewayAttachment:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      InternetGatewayId: !Ref LabIgw
      VpcId: !Ref LabVpc
```

#### Private Subnet
	- The configuration for the private subnet has no private routing attached to it. This is because by default, VPC creates a default route table which acts as a private route since it only has one rule ("local" route).

```YAML
##############################
# Private Subnet
##############################

  LabVpcPrivateSubnetA:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref LabVpc
      CidrBlock: !Ref PrivateSubnetCidr
      AvailabilityZone: us-west-2a
      Tags:
      - Key: Name
        Value: Private Subnet A
```

#### Security Group
	- The security group is added to the LabVpc with an Inbound Rule of Port 22 (SSH) allowed for all IPv4 addresses. The IpProtocol describes the transport protocol to be used and not the SSH as this is an application protocol.

```YAML
##############################
# Security Group
##############################

  LabSg:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Allow SSH to the public
      VpcId: !Ref LabVpc
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: '22'
          ToPort: '22'
          CidrIp: 0.0.0.0/0
```

#### EC2 Instance
	- The instance uses t3.micro as per laboratory requirements. The security group created earlier is attached although the EC2 instance is still not accessible via SSH because of the route table attached to the subnet used in this instance.

```YAML
##############################
# EC2 Instance
##############################

  LabInstance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !Ref AmazonLinuxAmiId
      InstanceType: t3.micro
      SecurityGroupIds:
        - !Ref LabSg
      SubnetId: !Ref LabVpcPrivateSubnetA
      Tags:
        - Key: Name
          Value: Lab Instance
```

## STEP 2: Upload the Stack in CloudFormation
1. Search for *CloudFormation* in AWS Management Console.

![unknown_asset](<assets/Pasted image 20261021140925.png>)

2. Under *Stack* navigation pane, select *Create Stack* at its main window.

![unknown_asset](<assets/Pasted image 20261021140937.png>)

3. A dropdown will appear and choose *With new resources (standard)*.

![unknown_asset](<assets/Pasted image 20261021140950.png>)

4. Under *Create Stack*, select the following configurations:
	- **Prepare template:** Select *Choose an existing template*.
	- **Template source:** Select *Upload a template file.* 
	- **Choose File:** Upload the file given earlier.

![unknown_asset](<assets/Pasted image 20261021141001.png>)

5. Click *Next*. Under the *Create Stack* step 2, provide the *Stack name*. After that, go straight to *Review and Create* to *submit*.

![unknown_asset](<assets/Pasted image 20261021141014.png>)

# Lessons Learned
- **Infrastructure as Code is repeatable.** One template can rebuild the whole environment, and deleting the stack cleans everything up in one step.
- **Parameters make templates reusable.** Moving the CIDR blocks and AMI ID into parameters means the template can be adapted without editing the resources.
- A subnet is **public** because of its route table. By default, a route table is **private**.
- It is not a good practice to use `0.0.0.0/0` for **Port 22** in security groups as it can made the system vulnerable to attacks. This was only configured because of the necessary specifications stated in the laboratory given by AWS.
- Not related to the laboratory but a **non-empty S3 buckets** will lead to a `DELETE_FAILED` status when its stack is deleted. To retain the S3 bucket while successfully deleting the stack, it should contain `DeletionPolicy:Retain` in its YAML file or use AWS CLI to delete the stack and add `--retain-resources <s3-logical-id`
- A **Configuration Drift** occurs when a resource configured by **IaC** is modified outside of CloudFormation (via AWS Console, CLI, or SDK)