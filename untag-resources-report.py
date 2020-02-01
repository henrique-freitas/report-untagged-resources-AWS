import sys
import boto3
from botocore.vendored import requests

##change tag what you want here 
needed_tags_on_s3 = ['Creator', 'Name', 'Status']
needed_tags_on_ec2 = ['Creator', 'Name', 'Status']
needed_tags_on_rds = ['Creator', 'Name', 'Status']
aws_regions_ec2 = ['sa-east-1', 'us-east-1']
aws_regions_rds = ['sa-east-1', 'us-east-1']
 
def lambda_handler(event, context):
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        bucket_name = (bucket['Name'])
        try:
            bucket_tagging = s3.get_bucket_tagging(Bucket=bucket_name)
            tag_set = bucket_tagging['TagSet']
            keys = []
            for tag in tag_set:    
                for key, value in iter(tag.items()): #tag.iteritems():
                    keys.append(value)
            applied_tags = keys[1::2]
            new_list = []
            for element in needed_tags_on_s3:
                if element not in applied_tags:
                    new_list.append(element)
            print("Tags list missed on Bucket:%s is %s" %(bucket_name, new_list))
            #f.write("Tags list missed on Bucket:%s is %s" %(bucket_name, new_list))
            #f.write("\n")
        except Exception as e:
            print("Tags list missed on Bucket:%s is %s" %(bucket_name, needed_tags_on_s3))
            #f.write("Tags list missed on Bucket:%s is %s" %(bucket_name, needed_tags_on_s3))
            #f.write("\n")
    for region in aws_regions_ec2:
        ec2 = boto3.client('ec2', region_name='sa-east-1')        
        response = ec2.describe_instances()
        instancelist = []
        for reservation in (response["Reservations"]):
            for instance in reservation["Instances"]:
                instancelist.append(instance["InstanceId"])
        for reservation in (response["Reservations"]):
            for instance in reservation["Instances"]:
                try:
                    tag_set = instance['Tags']
                    keys = []
                    for tag in tag_set:
                        for key, value in iter(tag.items()): #tag.iteritems():
                            keys.append(value)
                    applied_tags = keys[1::2]
                    new_list = []
                    for element in needed_tags_on_ec2:
                        if element not in applied_tags:
                            new_list.append(element)
                    print("AWS region is %s and Tags list missed on Instance ID :%s is %s" %(region, instance["InstanceId"], new_list))
                    #f.write("AWS region is %s and Tags list missed on Instance ID :%s is %s" %(region, instance["InstanceId"], new_list))
                    #f.write("\n")
                except Exception as e:
                    print ("AWS region is %s and Tags list missed on Instance ID :%s is %s" %(region, instance["InstanceId"], needed_tags_on_ec2))
    
                    #f.write("AWS region is %s and Tags list missed on Instance ID :%s is %s" %(region, instance["InstanceId"], needed_tags_on_ec2))
    
                    #f.write("\n")
 
    for region in aws_regions_rds:
        rds = boto3.client('rds', region_name='sa-east-1')
        response = rds.describe_db_instances();
        for dbinstances in (response["DBInstances"]):
            arn = dbinstances['DBInstanceArn']
            rds_description = rds.list_tags_for_resource(ResourceName=arn)
            tag_list = rds_description['TagList']
            keys = []
            for tag in tag_list:
                 for key, value in iter(tag.items()): #tag.iteritems():
                        keys.append(value)
            applied_tags = keys[1::2]
            new_list = []
            for element in needed_tags_on_rds:
                if element not in applied_tags:
                    new_list.append(element)
            print("AWS region is %s Tags list missed on RDS Instance ARN :%s is %s" %(region, arn, new_list))
            #f.write("AWS region is %s Tags list missed on RDS Instance ARN :%s is %s" %(region, arn, new_list))
            #f.write("\n")


