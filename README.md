# CSV2CF
## Overview
Writing cloudformation template to launch 100s of server is boring and cumbersome especially if your environment is already configured. I ran in to a similar situation and looking for solutions I found troposphere(https://github.com/cloudtools/troposphere). Which is python library that lets you generate cloudformation templates programmatically. This script uses troposphere to do the real magic.

##How to use
Make sure you have installed python3, pip, boto3 and troposphere.  
‘’’
yum install python3
yum install python3-pip
pip install boto3
pip install troposphere
‘’’
Configure an IAM user with access to your AMIs and configure its api keys from where your will run the script. If you do not do this the script will not be able to check the root drive of the AMI. Some AMIs are now coming with /dev/xvda as root drive instated of /dev/sda1. If the script is not able to read the AMIs it will default to /dev/sda1.
