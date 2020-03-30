def create_instances(client, gNames, tags, numOfIns,img_id='ami-0e2ff28bfb72a4e45'):
#
# gNames: list, eg: ['aa','bb']
# tags: list[dict], eg: [{}]
# numOfIns : int
    response = client.run_instances(
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/xvda',
                'VirtualName': 'Desktop',
                'Ebs': {
                    'DeleteOnTermination': True,
                    'VolumeSize': 8,
                    'VolumeType': 'gp2'
                },
            },
        ],
        ImageId=img_id,
        InstanceType='t2.micro',
        KeyName='TESTKEY',
        MaxCount= numOfIns,
        MinCount=1,
        Monitoring={
            'Enabled': False
        },
        SecurityGroups=gNames,
        TagSpecifications=tags
    )
    n = len(response['Instances'])

    if n == 1:
        print('1 instance has been created.')
    elif  n == numOfIns:
        print('%s instances have been created.'%(n))    
    elif n < numOfIns: 
        print('Exceed the max, %s instances have been created.'%(n))
    else:
        print('Failed.')
    
    ins_ids = []
    for i in range(n): 
        ins_id = response['Instances'][i]['InstanceId']
        ins_ids.append(ins_id)
        
    return ins_ids

################
#check instance status
def describe_instance_status(client,ins_ids):
    response = client.describe_instance_status(
        InstanceIds=ins_ids,
        IncludeAllInstances=True
    )
    
    dic = {}
    instance_id = response['InstanceStatuses'][0]['InstanceId']
    status = response['InstanceStatuses'][0]['InstanceState']['Name']
    dic[instance_id] = status
    
    return dic



################
#Stop the instance
def stop_instances(client,ins_ids):
#input:
#  ins_ids: list, the id of the instances to be stoped
#output:
# status: dictionary, the id and the status
    response = client.stop_instances(
        InstanceIds=ins_ids
    )
    dic = {}
    instance_id = response['StoppingInstances'][0]['InstanceId']
    status = response['StoppingInstances'][0]['CurrentState']['Name']
    dic[instance_id] = status
    return dic
##############################################################################
'''
import boto3 
import time

def main():
    client = boto3.client('ec2', region_name='us-east-1')

    gNames = ['cr01-sg']
    tags = [
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'test3'
                    }
                ]
            }
            ]

    numOfIns = 1
    r = create_instances(client, gNames, tags, numOfIns)
    n = len(r['Instances'])

    if n == 1:
        print('1 instance has been created.')
    elif  n == numOfIns:
        print('%s instances have been created.'%(n))    
    elif n < numOfIns: 
        print('Exceed the max, %s instances have been created.'%(n))
    else:
        print('Failed.')
    
    # get ins_ids
    ins_ids = []
    ins_id = r['Instances'][0]['InstanceId']
    ins_ids.append(ins_id)

    # check the state whether is running
    print('Check the status:')
    for i in range(10):
        res = describe_instance_status(client,ins_ids)
        print(res)
        if res[ins_ids[0]] == 'running': break
        time.sleep(10)
        i += 1


    # stop the instance
    print('Stop the instance:')
    res = stop_instances(client,ins_ids)
    print(res)

main()

'''