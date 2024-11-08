import boto3
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def list_instances(ec2):
    return [(instance.id, instance.instance_type, instance.state['Name']) for instance in ec2.instances.all()]


def available_zones():
    ec2 = boto3.client('ec2')
    return [zone['ZoneName'] for zone in ec2.describe_availability_zones()['AvailabilityZones']]

def start_instance(ec2, instance_id):
    return None


def stop_instance(ec2, instance_id):
    return None


def create_instance(ec2, image_id, instance_type):
    return None


def reboot_instance(ec2, instance_id):
    return None


def list_images(ec2):
    return None


def condor_status_check():
    return None


def do_some_job():
    return None


def main():
    ec2 = boto3.resource('ec2')
    while True:
        clear_screen()
        print("\nAmazon AWS Control Panel Using SDK")
        print("1. List Instances")
        print("2. Available Zones")
        print("3. Start Instance")
        print("4. Available Regions")
        print("5. Stop Instance")
        print("6. Create Instance")
        print("7. Reboot Instance")
        print("8. List Images")
        print("9. Condor Status Check")
        print("10. Do Some Job")
        print("99. Quit")
        input_str = input("Enter an integer: ")

        if input_str == '1':
            for instance in list_instances(ec2):
                print(f"Instance ID : {instance[0]}, Instance Type : {instance[1]}, Instance State : {instance[2]}")
        elif input_str == '2':
            print(f"Available Zones")
            for zone in available_zones():
                print(zone)
        elif input_str == '3':
            pass
        elif input_str == '5':
            pass
        elif input_str == '6':
            pass
        elif input_str == '7':
            pass
        elif input_str == '8':
            pass
        elif input_str == '9':
            pass
        elif input_str == '10':
            pass
        elif input_str == '99':
            break
        else:
            print("Invalid option. Please try again.")

        input("Press any key to continue...")

if __name__ == "__main__":
    main()

