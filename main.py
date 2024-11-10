import boto3
import os
import paramiko
import time
import scp


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def list_instances(ec2):
    return [(instance.id, instance.instance_type, instance.state['Name']) for instance in ec2.instances.all()]


def available_zones():
    ec2 = boto3.client('ec2')
    return [zone['ZoneName'] for zone in ec2.describe_availability_zones()['AvailabilityZones']]


def available_regions():
    return boto3.Session().get_available_regions('ec2')


def start_instance(ec2, instance_id):
    chk = False
    for instance in list_instances(ec2):
        if instance[0] == instance_id:
            chk = True
    if chk:
        ec2.Instance(instance_id).start()
        print(f"Instance {instance_id} started")
    else:
        print(f"Error : No valid instance ID")


def stop_instance(ec2, instance_id):
    chk = False
    for instance in list_instances(ec2):
        if instance[0] == instance_id:
            chk = True
    if chk:
        ec2.Instance(instance_id).stop()
        print(f"Instance {instance_id} stopped")
    else:
        print("Error : No valid instance ID")


def create_instance(ec2, image_id):
    chk = False
    for image in list_images()['Images']:
        if image['ImageId'] == image_id:
            chk = True
    if chk:
        Instance = ec2.create_instances(ImageId=image_id, InstanceType='t2.micro', MinCount=1, MaxCount=1, KeyName='cloud-test', SecurityGroupIds=['HTCondor'])
        print(f"Instance {Instance[0].id} created")
    else:
        print("Error : No valid image ID")


def reboot_instance(ec2, instance_id):
    chk = False
    for instance in list_instances(ec2):
        if instance[0] == instance_id:
            chk = True
    if chk:
        ec2.Instance(instance_id).reboot()
        print(f"Instance {instance_id} rebooted")
    else:
        print("Error : No valid instance ID")


def list_images():
    return boto3.client('ec2').describe_images(Owners=['self'])


def condor_status_check(ec2, instance_id):
    chk = False
    for instance in list_instances(ec2):
        if instance[0] == instance_id:
            chk = True
    if not chk:
        print(f"Instance {instance_id} is not exist")
        return None
    ec2c = boto3.client('ec2')
    instance = ec2c.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
    key = paramiko.RSAKey.from_private_key_file("******mask for upload git******")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=instance["PublicIpAddress"], username='***mask***', pkey=key)
        stdin, stdout, stderr = ssh.exec_command('condor_status')
        print(stdout.read().decode())
    except Exception as e:
        print(f"{e}")
    finally:
        ssh.close


def do_some_job(ec2, instance_id):
    chk = False
    for instance in list_instances(ec2):
        if instance[0] == instance_id:
            chk = True
    if not chk:
        print(f"Instance {instance_id} is not exist")
        return None
    ec2c = boto3.client('ec2')
    instance = ec2c.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
    key = paramiko.RSAKey.from_private_key_file("******mask for upload git******")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=instance["PublicIpAddress"], username='***mask***', pkey=key)
    total = 0
    nump = int(input("Input Process Number : "))
    with scp.SCPClient(ssh.get_transport()) as scpp:
        scpp.put("./count.sh", "/home/***mask***/count.sh")
    try:
        for i in range(nump):
            num_start = i * 10
            num_end = num_start + 9
            cmd = f'condor_submit -a "executable=/home/***mask***/count.sh" -a "universe=vanilla" -a "arguments={num_start} {num_end}" -a "output=/home/***mask***/out.{i}.txt" -a "error=/home/***mask***/err.{i}.txt" -a "log=/home/***mask***/log.{i}.log" -a "queue 1"'
            ssh.exec_command(cmd)
            print(f"Job{i} submitted")
        print(f"Sleep 5 Seconds...")
        time.sleep(5)
        for i in range(nump):
            cmd = f'cat /home/***mask***/out.{i}.txt'
            stdin, stdout, stderr = ssh.exec_command(cmd)
            for line in stdout.read().decode().splitlines():
                print(line)
                if "Total Sum =" in line:
                    total += int(line.split('=')[1].strip())
        print(f"Big Total Sum = {total}")

    except Exception as e:
        print(f"{e}")
    finally:
        ssh.close


def main():
    ec2 = boto3.resource('ec2')
    while True:
        clear_screen()
        print("\nAmazon AWS Control Panel Using SDK")
        print("1. List Instances")
        print("2. Available Zones")
        print("3. Available Regions")
        print("4. Start Instance")
        print("5. Stop Instance")
        print("6. Create Instance")
        print("7. Reboot Instance")
        print("8. List Images")
        print("9. Condor Status Check")
        print("10. Do Custom Job")
        print("99. Quit")
        input_str = input("Enter an integer: ")

        if input_str == '1':
            print(f"List All Instances")
            for instance in list_instances(ec2):
                print(f"Instance ID : {instance[0]}, Instance Type : {instance[1]}, Instance State : {instance[2]}")
        elif input_str == '2':
            print(f"Available Zones")
            for zone in available_zones():
                print(f"{zone}")
        elif input_str == '3':
            print(f"Available Regions")
            for region in available_regions():
                print(f"{region}")
        elif input_str == '4':
            print(f"Start Instance \n ============")
            print(f"List All Instances")
            for instance in list_instances(ec2):
                print(f"Instance ID : {instance[0]}, Instance Type : {instance[1]}, Instance State : {instance[2]}")
            start_instance(ec2, str(input("Input Instance ID : ")))       
        elif input_str == '5':
            print(f"Stop Instance \n ============")
            print(f"List All Instances")
            for instance in list_instances(ec2):
                print(f"Instance ID : {instance[0]}, Instance Type : {instance[1]}, Instance State : {instance[2]}")
            stop_instance(ec2, str(input("Input Instance ID : ")))       
        elif input_str == '6':
            print(f"Create Instance \n ============")
            print(f"List All Available Images")
            for image in list_images()['Images']:
                print(f"AMI ID : {image['ImageId']}, Name : {image['Name']}")
            create_instance(ec2, str(input("Input Image ID : ")))       
        elif input_str == '7':
            print(f"Reboot Instance \n ============")
            print(f"List All Instances")
            for instance in list_instances(ec2):
                print(f"Instance ID : {instance[0]}, Instance Type : {instance[1]}, Instance State : {instance[2]}")
            reboot_instance(ec2, str(input("Input Instance ID : ")))       
        elif input_str == '8':
            print(f"List All Available Images")
            for image in list_images()['Images']:
                print(f"AMI ID : {image['ImageId']}, Name : {image['Name']}")
        elif input_str == '9':
            print(f"Condor Status Check \n ============")
            print(f"List All Instances")
            for instance in list_instances(ec2):
                print(f"Instance ID : {instance[0]}, Instance Type : {instance[1]}, Instance State : {instance[2]}")
            condor_status_check(ec2, str(input("Input Instance ID : ")))       
        elif input_str == '10':
            print(f"Do Custom Job \n ============")
            print(f"List All Instances")
            for instance in list_instances(ec2):
                print(f"Instance ID : {instance[0]}, Instance Type : {instance[1]}, Instance State : {instance[2]}")
            do_some_job(ec2, str(input("Input Instance ID : ")))       
        elif input_str == '99':
            print(f"@program shutdown@ - Hyunsa")
            break
        else:
            print("Invalid option. Please try again.")

        input("Press any key to continue...")

if __name__ == "__main__":
    main()

