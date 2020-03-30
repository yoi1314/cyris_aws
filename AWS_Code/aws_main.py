import boto3
import time
import json
from aws_sg import create_security_group, edit_ingress, describe_security_groups
from aws_instances import create_instances, describe_instance_status, stop_instances
from aws_image import create_img, describe_image
from aws_info import edit_tags, get_info
 
def main():
    
    client = boto3.client('ec2', region_name='us-east-1')

    # create a security group
    gName = 'cr01-sg' # example
    status = create_security_group(client, gName)
    print(status)

    # edit ingress
    edit_ingress(client, gName)

    # describe_security_groups get
    gNames = []
    gNames.append(gName) # example:['cr01-sg']

    r = describe_security_groups(client, gNames)
    ipPermissions = r['SecurityGroups'][0]['IpPermissions']
    if ipPermissions:
        print('Edit security group ingress successfully.')
    else:
        print('Edit security group ingress failed.')
##############################################################################################################################
    # create an instance
    tags = [
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'cr01'
                    }
                ]
            }
            ]

    numOfIns = 1

    ins_ids = create_instances(client, gNames, tags, numOfIns)

    # check the state whether is running
    print('Check the status:')
    for i in range(10):
        res = describe_instance_status(client,ins_ids)
        print(res)
        if res[ins_ids[0]] == 'running': break
        time.sleep(10)


    # stop the instance
    print('Stop the instance:')
    res = stop_instances(client,ins_ids)

    # check whether stopped
    for i in range(10):
            res = describe_instance_status(client,ins_ids)
            print(res)
            if res[ins_ids[0]] == 'stopped': break
            time.sleep(10)

##############################################################################################################################
    # create(clone) image
    img_id = create_img(client,ins_ids[0])
    
    # check the image state whether is running
    print('Check the cloned image status:')
    for i in range(20):
        res = describe_image(client, img_id)
        print(res)
        if res[img_id] == 'available': break
        time.sleep(10)

##############################################################################################################################
#   create instances based on the new imageId. 
    print('Create instances based on the cloned image')
    tags = [
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': '#cr01'
                    }
                ]
            }
            ]
    numOfIns = 2
    ins_ids = create_instances(client, gNames, tags, numOfIns,img_id)
    length = len(ins_ids)

    # edit the tags
    for i in range(length):
        ins_id = ins_ids[i]
        v = '#cr01-' + str(i)
        edit_tags(client, ins_id, v)
    # success edited(feedback?)

    # get ip and output to file
    data = get_info(client)
    with open('ip_info.json', 'w') as f:
        json.dump(data, f)
#location?
    # success writed(feedback?)
    
if __name__ == "__main__":
    main()
