#
# author: Hazaq Naeem <hazaq@integratech.ae>
# Reads a CSV file with a list of ec2 and generates \
# a Cloudformation template. This script requires 2 argument the location of the \
# CSV file and output location of cloudformation template 
# CSV should be in below order
# Name: Can be name to represent the cloudformation block, should be a unique name
# AMI: AMI to use for the ec2
# Type: EC2 instance type example t2.micro, m4.large
# Security group: Security group id attached to the EC2
# Key Pair: Key pair to use
# Subnet: Subnet ID to use, where ec2 will be launched
# EBS Disk: Root volume disk
# TAGs: Tags in this order (Default empty) Name,OS,Env,Role
# OS is a must have tag 

import csv
import boto3
import argparse
from troposphere import Ref, Template, Base64
import troposphere.ec2 as ec2

t = Template()
client = boto3.client('ec2')

parser = argparse.ArgumentParser(description='EC2 CSV to CloudFormation script')
parser.add_argument('csv_location',metavar='CSV Location',type=str,help='Location of the csv file')
parser.add_argument('out_cf',metavar='Output Location',type=str,nargs='?',default=\
    'cloudformation.template',help='Location of the output Cloudformation template')
args = parser.parse_args()
csv_location = args.csv_location
out_cf = args.out_cf

cf_version = "AWSTemplateFormatVersion: 2010-09-09"


def os_check(tag_os,count):
    if (tag_os == "Linux") or (tag_os == "linux"):
        user_data = Base64('#!/bin/bash')
        return ('linux', user_data)
    elif (tag_os == "Windows") or (tag_os == "windows"):
        user_data = Base64('<powershell> </powershell>') 
        return ('win', user_data)
    else:
         print (f"ERROR: Invalid OS Tag at line: {count}, Valid options \"Linux\"|\"Windows\" ")
         exit()

def root_dev(ami_id, count):
    try: 
        image_data = client.describe_images( ImageIds=[ ami_id ] )
        return (image_data['Images'][0]['RootDeviceName'])
    except:
        print(f"WARNING: Can't access AMI {ami_id} using access keys on line: {count} using /dev/sda1 as root device")
        return ("/dev/sda1")


with open(csv_location) as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f"Reading {csv_location}.........")
            print (f'CSV definition ROW\n{", ".join(row)}')
            line_count += 1
        else:
            ec2_name = row[0]
            ec2_ami = row[1]
            ec2_type = row[2]
            ec2_sg = row[3]
            ec2_key = row[4]
            ec2_subnet = row[5]
            ec2_ebs_disk = int(row[6])
            ec2_tag_name =row[7]
            ec2_tag_os = row[8]
            ec2_tag_env = row[9]
            ec2_tag_role = row[10]
            ec2_os_check = os_check(ec2_tag_os, line_count)
            ec2_iam = ec2_os_check[0]
            ec2_user_data = ec2_os_check[1]
            ec2_root_dev = root_dev(ec2_ami, line_count)
            instance = ec2.Instance(ec2_name,ImageId=ec2_ami,InstanceType=ec2_type,\
                        SecurityGroupIds=[ec2_sg],KeyName=ec2_key,SubnetId=ec2_subnet,\
                        BlockDeviceMappings=[{ "DeviceName" : ec2_root_dev, "Ebs" :{"DeleteOnTermination" : True,\
                        "VolumeSize" : ec2_ebs_disk, "VolumeType" : "gp2", "Encrypted" : True} }],\
                            IamInstanceProfile=ec2_iam, UserData=ec2_user_data,\
                        Tags=[{"Key" : "Name", "Value" : ec2_tag_name  }, {"Key" : "OS", "Value" : ec2_tag_os},\
                            {"Key" : "Env", "Value" : ec2_tag_env }, {"Key" : "Role", "Value" : ec2_tag_role }]
                        )
            try:
                t.add_resource(instance)
            except ValueError as e:
                print(f"ERROR: {e} at line {line_count} ")
                exit()
            line_count += 1


print("Generating the CloudFormation template.........")
cf = open(out_cf,'w')
print(cf_version,file=cf)
print(t.to_yaml(),file=cf)
print(f"{out_cf} Finished with SUCCESS.")
cf.close()
