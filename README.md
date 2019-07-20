# CSV2CF
## Overview
Writing cloudformation template to launch 100s of server is boring and cumbersome especially if your environment is already configured. I ran in to a similar situation and looking for solutions I found troposphere(https://github.com/cloudtools/troposphere). Which is python library that lets you generate cloudformation templates programmatically. This script uses troposphere to do the real magic.  

## How to use  
Make sure you have installed python3, pip, boto3 and troposphere.  
```
yum install python3
yum install python3-pip
pip install boto3
pip install troposphere
```
Configure an IAM user with access to your AMIs and configure its api keys from where your will run the script. If you do not do this the script will not be able to check the root drive of the AMI. Some AMIs are now coming with /dev/xvda as root drive instated of /dev/sda1. If the script is not able to read the AMIs it will default to /dev/sda1.  
The csv file should in the below given order
Name: Can be a name to represent the cloudformation block, should be a unique name  
AMI: AMI to use for the ec2  
Type: EC2 instance type example t2.micro, m4.large  
Security group: Security group id attached to the EC2  
Key Pair: Key pair to use  
Subnet: Subnet ID to use, where ec2 will be launched  
EBS Disk: Root volume disk  
TAGs: Tags in this order (Default empty) **Name**,**OS**,**Env**,**Role**  
**OS** is a must have tag  

An example csv is given as part of the script.  

### Example  
```
python3 CFGen.py ec2list.csv cloud.template 
```
