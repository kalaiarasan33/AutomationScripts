import boto3
import logging
import os
import datetime


client= boto3.client('ec2')

server_name=input('Enter the hostname: ')

date=datetime.datetime.now()
date_format=str(date.strftime("%Y%m%d"))
path="D:\\log"
log_file="ec2state" + date_format
log_path_file=os.path.join(path,log_file)
logging.basicConfig(filename=log_path_file,level=logging.INFO,format='%(asctime)s - %(levelname)s %(message)s') 


for x in client.describe_instances( Filters=[{'Name': 'tag:Name','Values': [server_name]},])['Reservations']:
    for y in x['Instances']:
        instance_id=y['InstanceId']
        instance_state=y['State']['Name']
        logging.info('Native status of instance : %s , %s , %s' %(server_name,instance_id,instance_state))

action=input('please enter the action start ,stop , restart : ')

try:



 if instance_state == 'stopped':
   if action== 'start':

    try:
       logging.info('server starting has been initiated, please wait: %s - %s ' %(server_name,instance_id))
       startinstance = client.start_instances(InstanceIds=[instance_id,])
       logging.info('server starting has been completed, please wait for few min: %s - %s ' %(server_name,instance_id))
       print('server starting has been completed, please wait for few min: %s - %s ' %(server_name,instance_id))
    except:
       logging.critical('due to error , not able to start: %s - %s ' %(server_name,instance_id))
     
 elif instance_state == 'running':

    if action == 'restart' :

        try:
           logging.info('server restarting has been initiated, please wait: %s - %s ' %(server_name,instance_id))
           stop_instance = client.reboot_instances(InstanceIds=[instance_id,])
           logging.info('server restarting has been completed, please wait for few min: %s - %s ' %(server_name,instance_id))
           print('server restarting has been completed, please wait for few min: %s - %s ' %(server_name,instance_id))
        except:
          logging.critical('due to error , not able to restart%s - %s ' %(server_name,instance_id))

    elif action == 'stop':
      try:
       logging.info('server stopping has been initiated, please wait: %s - %s ' %(server_name,instance_id))
       stop_instance = client.stop_instances(InstanceIds=[instance_id,])
       logging.info('server stopping has been completed, please wait for few min: %s - %s ' %(server_name,instance_id))
       print('server stopping has been completed, please wait for few min: %s - %s ' %(server_name,instance_id))
      except:
       logging.critical('due to error , not able to restart')


 elif instance_state == 'terminated':
      print('please check the instance is terminated: %s - %s ' %(server_name,instance_id))
      logging.debug('please check the instance is terminated: %s - %s ' %(server_name,instance_id) )

 elif instance_state == 'pending':

     print('please check the instance is pending status: %s - %s ' %(server_name,instance_id) )
     logging.debug('please check the instance is pending status: %s - %s ' %(server_name,instance_id) )

 elif instance_state == 'stopping':
     print('please check the instance is stopping status: %s - %s ' %(server_name,instance_id))
     logging.debug('please check the instance is stopping status: %s - %s ' %(server_name,instance_id) )

 elif instance_state == 'shutting-down':
     print('please check the instance is shutting-down: %s - %s ' %(server_name,instance_id) )
     logging.debug('please check the instance is shutting-down: %s - %s ' %(server_name,instance_id) )

except:
     print('please check , servername is not available in ec2: %s  ' %(server_name) )
     logging.debug('please check , servername is not available in ec2: %s ' %(server_name) )