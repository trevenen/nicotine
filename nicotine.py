import clearance
import sys
import vapor_modes
import typing

# TO-DO:
# 1) consider pretty printing in vapors.log?
# 2) vaporize clearance

def main():
    clearance.check_botocore()
    clearance.check_boto3()
    clearance.check_credentials()
    clearance.check_fed()
    clearance.check_fed_version()
    arg()
    doctors()
    ami_timestamp()
    session = boto3.session.Session(profile_name=arg.env)
    client = session.client(AWS_SERVICE)
    resource = session.resource(AWS_SERVICE)
    instance = resource.Instance(arg.instance_id)
    name(client)
    ami_name(name.n)
    #create_ami(ami_name.n)
    #test_ami(create_ami.id)

if __name__ == '__main__':
    main()
