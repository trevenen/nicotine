import smoker
import sys
import vapor
import vapor_modes
import typing

from clearance import Clearance
from doctor import Doctor
from smoker import smoker, secret

# TO-DO:
# 1) consider pretty printing in vapors.log?
# 2) vaporize clearance

def main():
    # smoker is not
    # a class and does not
    # have vapors
    try:
        smoke = smoker()
        vapor.vapors('smoker instantiated successfully')
    except Exception as e:
        vapor.vapors('smoker instantiation failed', e)
        raise

    try:
        sec = secret()
        vapor.vapors('secrets collected successfully')
    except Exception as e:
        vapor.vapors('failed to collect secrets', e)
        raise

    # try/excepts are built-in
    # unlike with smoker
    # passing
    clear = Clearance('/Users/a6878zz/.aws/credentials', '/usr/local/bin/fed')
    clear.check_botocore()
    clear.check_boto3()
    clear.check_credentials()
    clear.check_fed()
    clear.check_fed_version()

    # try/except
    # not built-in to
    # Doctor class
    try:
        doc = Doctor(smoke.env, smoke.instance_id)
        vapor.vapors('doctor instantiation successful')
    except Exception as e:
        vapor.vapors('doctor instantiation failed', e)
        raise

    try:
        client = doc.create_client()
        vapor.vapors(f'boto3 {smoke.service} client instantiation successful')
    except Exception as e:
        vapor.vapors(f'boto3 {smoke.service} client instantiation failed', e)
        raise

    try:
        res = doc.create_resource()
        vapor.vapors('boto3 {smoke.service} resource instantiation successful')
    except Exception as e:
        vapor.vapors('boto3 {smoke.service} resource instantiation failed', e)
        raise

    try:
        instance = doc.create_instance()
        vapor.vapors('boto3 {smoke.service} instance instantiation successful')
    except Exception as e:
        vapor.vapors('boto3 {smoke.service} instance instantiation failed', e)
        raise



    #arg()
    #doctors()
    #ami_timestamp()
    #session = boto3.session.Session(profile_name=arg.env)
    #client = session.client(AWS_SERVICE)
    #resource = session.resource(AWS_SERVICE)
    #instance = resource.Instance(arg.instance_id)
    #name(client)
    #ami_name(name.n)
    #create_ami(ami_name.n)
    #test_ami(create_ami.id)

if __name__ == '__main__':
    main()
