import boto3
import csv

ec2=boto3.client('ec2')
s_no=1
file=open('iAws.csv','w')
header=['s_no','instance_name','instance_imageid','instance_id','instance_type','instance_volume_id','instance_vpc_id','instance_security_grpname','instance_current_state']
csv_w=csv.writer(file, lineterminator='\n')
csv_w.writerow(header)
for x in ec2.describe_instances()['Reservations']:
   try:
    for inst in x['Instances']:
        ins_imgid=inst['ImageId']
        ins_id=inst['InstanceId']
        ins_type=inst['InstanceType']
        ins_state=inst['State']['Name']
        '''  filtering  in Tags [{'Key': 'Name', 'Value': 'linuxprod'}, {'Key': 'project', 'Value': 'test'}]  with help of len function checking total length
        then using range funtion passing as array index, checking in  dictionary key should be 'Name, if tag key as Name then  storing value in variable'
        '''
        tag_len=len(inst['Tags'])
        print(inst['Tags'])
        for r in range(0,tag_len):
            if inst['Tags'][r]['Key'] == 'Name':
               ins_name=inst['Tags'][r]['Value']
        ins_vpcid=inst['VpcId']
        for ivol in inst['BlockDeviceMappings']:
            ins_volid=ivol['Ebs']['VolumeId']
        for isec in inst['SecurityGroups']:
            ins_secgrp=isec['GroupName']
    print(s_no,ins_name,ins_imgid,ins_id,ins_type,ins_volid,ins_vpcid,ins_secgrp,ins_state)
    csv_w.writerow([s_no,ins_name,ins_imgid,ins_id,ins_type,ins_volid,ins_vpcid,ins_secgrp,ins_state])
    s_no=s_no+1
   except:
    print(s_no,ins_imgid,ins_id,ins_type,ins_state)
    csv_w.writerow([s_no,ins_name,ins_imgid,ins_id,ins_type,'null','null','null',ins_state])
    s_no=s_no+1