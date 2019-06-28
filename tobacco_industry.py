import argparse
import boto3
import pprint
import sys

parser = argparse.ArgumentParser(description='smoker: launch a box, cancer: kill a box')

# for future features
parser.add_argument('-c',
    help='aws API client to instantiate',
    type=str, action='store',
    dest='client', required=False)

parser.add_argument('-i',
    help='instance id of the smoker to kill',
    type=str, action='store',
    dest='instance_id', required=False)

parser.add_argument('-n',
    help='short name of the instance',
    type=str, action='store',
    dest='smoker_name', required=True)

parser.add_argument('-r',
    help='resource',
    type=str, action='store',
    dest='resource', required=False)

parser.add_argument('--dry-run',
    help='first cigarette or immune to cancer?',
    type=str, action='store',
    dest='dry_run', required=False, default=False)

args = parser.parse_args()

if not args.client:
    args.client = 'ec2'

def profile() -> str:
    for env in ['-dev-', '-qa-', '-prod-']:
        if env in args.smoker_name:
            profile = env.split('-')[1]
            return profile
    raise ProfileNotFound('smoker name\n' + \
                          'instance short name\n' + \
                          'did not contain an\n' + \
                          'environment short name.')

session = boto3.session.Session(profile_name=profile())
client = session.client(args.client)

# feature not built
# out yet
#if args.resource:
#    resource = session.resource(args.resource)

# feature not built
# out yet
#if args.instance_id:
#    resource_instance = resource.Instance(args.instance_id)

def smoker(image_id='ami-**********',
           instance_type='t2.micro',
           min_count=1,
           max_count=1,
           associate_public_ip_address=False,
           tag_specification=[],
           iam_instance_profile={'Name': 'some_role'},
           dry_run=False
           ) -> dict:

    tag_specification = [{'ResourceType': 'instance',
                         'Tags': [
                            {
                                 'Key': 'Environment',
                                 'Value': profile()
                            },
                            {
                                 'Key': 'OperatingSystem',
                                 'Value': 'linux'
                            },
                            {
                                 'Key': 'ID',
                                 'Value': 'INT'
                            },
                            {
                                 'Key': 'ApplicationName',
                                 'Value': 'NAME'
                            },
                            {
                                 'Key': 'Name',
                                 'Value': args.smoker_name
                            },
                            {
                                 'Key': 'ProductOwnerEmail',
                                 'Value': 'you@domain.com'
                            },
                            {
                                'Key': 'AlternateEmail',
                                 'Value': 'other@domain.com'
                            }
                        ]
                    }
                ]

    response = client.run_instances(ImageId=image_id,
                        NetworkInterfaces=[{
                        'AssociatePublicIpAddress': associate_public_ip_address,
                        'DeviceIndex': 0,
                        'Groups': [''],
                        'SubnetId': ''
                        }],
                        InstanceType=instance_type,
                        MaxCount=max_count,
                        MinCount=min_count,
                        IamInstanceProfile=iam_instance_profile,
                        DryRun=dry_run,
                        TagSpecifications=tag_specification
                        )

    pprint.pprint(response)

def cancer(instance_ids=[args.instance_id], dry_run=args.dry_run) -> dict:

    response = client.terminate_instances(InstanceIds=instance_ids, DryRun=dry_run)

# live or die
if args.smoker_name and args.instance_id:
    cancer()
elif args.smoker_name:
    smoker()
else:
    print('either smokes or has cancer: not both nor neither')
