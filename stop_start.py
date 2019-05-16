import boto3
ec2= boto3.resource('ec2')
sns = boto3.client('sns')
cloudtrail = boto3.client('cloudtrail')

ins_sid = [] 
ins_tid = [] 
for inst in ec2.instances.all():  
  try:
    if inst.state['Name'] == 'stopped' or inst.state['Name'] == 'terminated': #filtering  the instance if stopped and terminated
      try: 
        if inst.state['Name'] == 'stopped':
            ins_sid.append(inst.id) # appending and storing the instance id in list ins_sid  for stopped instance
            len_tags=len(inst.tags) # checking len of tag
            for x in range(0,len_tags):
                if inst.tags[x]['Key'].lower() == 'maintenance' and inst.tags[x]['Value'].lower() == 'true': #filtering the tag if key as maintenance and value as true
                    ins_sid.remove(inst.id) # deleting the instance id in list if condition is true
            for i in ins_sid: # now we  filtered case stoped , terminated 
                i_id='please check the instance id {}'.format(i)
                cloud_trail_events = cloudtrail.lookup_events(LookupAttributes=[{'AttributeKey': 'ResourceName','AttributeValue': i} and {'AttributeKey': 'EventName','AttributeValue': 'StopInstances' }],MaxResults=1,) 
                for x in cloud_trail_events['Events']:
                    Access_key="AccessKeyId = {}".format(x['AccessKeyId'])
                    Event_name="EventName = {}".format(x['EventName'])
                    User_name="Username = {}".format(x['Username'])  
                    i_message= "\n    {0},\n    {1},\n    {2},\n    {3}".format(i_id,Event_name,User_name,Access_key)    
                    send_email = sns.publish(TargetArn='arn:aws:sns:us-west-2:054390801093:ec2_lambda',Message=i_message,Subject='instance has been stopped or terminated')
      except:
          print("Error")
      try:
        if inst.state['Name'] == 'terminated':
            ins_tid.append(inst.id) # appending and storing the instance id in list ins_tid for terminated
            len_tags=len(inst.tags) # checking len of tag
            for x in range(0,len_tags):
                if inst.tags[x]['Key'].lower() == 'maintenance' and inst.tags[x]['Value'].lower() == 'true': #filtering the tag if key as maintenance and value as true
                    ins_tid.remove(inst.id) # deleting the instance id in list if condition is true
            for i in ins_tid: # now we  filtered case stoped , terminated 
                i_id='please check the instance id {}'.format(i)
                cloud_trail_events = cloudtrail.lookup_events(LookupAttributes=[{'AttributeKey': 'ResourceName','AttributeValue': i} and {'AttributeKey': 'EventName','AttributeValue': 'TerminateInstances' }],MaxResults=1,) 
                for x in cloud_trail_events['Events']:
                    Access_key="AccessKeyId = {}".format(x['AccessKeyId'])
                    Event_name="EventName = {}".format(x['EventName'])
                    User_name="Username = {}".format(x['Username'])  
                    i_message= "\n    {0},\n    {1},\n    {2},\n    {3}".format(i_id,Event_name,User_name,Access_key)    
                    send_email = sns.publish(TargetArn='arn:aws:sns:us-west-2:054390801093:ec2_lambda',Message=i_message,Subject='instance has been stopped or terminated')
      except:
          print("Error")
  except:
     print('no instance in stopped and terminated state')
        


