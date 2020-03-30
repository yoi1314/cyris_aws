def create_img(client,ins_id, des='The new image create from the previous_instance(BaseVM)', name='basevm_cloned'):

    response = client.create_image(
        Description=des,
        InstanceId=ins_id,
        Name=name,
        #NoReboot=True|False
    )
    img_id = response['ImageId']
    return img_id


#########################

def describe_image(client, img_id):
    response = client.describe_images(
        ImageIds=[
            img_id,
        ]
    )
    dic = {}
    dic[img_id] = response['Images'][0]['State']
    
    return dic

#test
