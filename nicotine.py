import smoker
import sys
import vapor
import vapor_modes
import typing

from clearance import Clearance
from doctor import Doctor
from nicotine_patch import NicotinePatch
from prep_epinephrine import PrepEpinephrine
from smoker import smoker, secret

# TO-DO:
# 1) consider pretty printing in vapors.log?
# 2) vaporize clearance

def main():
    # smoker is not
    # a class and does not
    # have vapors
    #
    # passing
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
    #
    # passing
    clear = Clearance('/Users/me/.aws/credentials', '/usr/local/bin/fed')
    clear.check_botocore()
    clear.check_boto3()
    clear.check_credentials()
    clear.check_fed()
    clear.check_fed_version()

    # try/except
    # not built-in to
    # Doctor class
    #
    # passing
    try:
        doc = Doctor(smoke.env, smoke.instance_id)
        vapor.vapors('doctor instantiation successful')
    except Exception as e:
        vapor.vapors('doctor instantiation failed', e)
        raise

    try:
        client = doc.create_client()
        vapor.vapors(f'boto3 {doc.service} client instantiation successful')
    except Exception as e:
        vapor.vapors(f'boto3 {doc.service} client instantiation failed', e)
        raise

    try:
        res = doc.create_resource()
        vapor.vapors(f'boto3 {doc.service} resource instantiation successful')
    except Exception as e:
        vapor.vapors(f'boto3 {doc.service} resource instantiation failed', e)
        raise

    try:
        instance = doc.create_instance()
        vapor.vapors(f'boto3 {doc.service} instance instantiation successful')
    except Exception as e:
        vapor.vapors(f'boto3 {doc.service} instance instantiation failed', e)
        raise

    try:
        prep = PrepEpinephrine(smoke.env, smoke.instance_id, client)
        vapor.vapors('epinephrine successfully prepped')
    except Exception as e:
        vapor.vapors('epinephrine prep failed', e)
        raise

    # built-in try/except
    timestamp = prep.create_ami_timestamp()
    tags = prep.get_tags()
    name = prep.check_name(tags)
    ami_name = prep.ami_name(name, timestamp)
    ami_id = prep.create_ami(ami_name)
    prep.test_ami(ami_name, ami_id)

    try:
        nic = NicotinePatch(smoke.env, smoke.instance_id,
                              client, instance)
        vapor.vapors('nicotine patch instantiated '
                     'successfully')
    except Exception as e:
        vapor.vapors('nicotine patch instnatiation '
                     'failed.', e)
        raise








    #ami_timestamp()
    #name(client)
    #ami_name(name.n)
    #create_ami(ami_name.n)
    #test_ami(create_ami.id)

if __name__ == '__main__':
    main()
