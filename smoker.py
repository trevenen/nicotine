import argparse
import getpass
import sys
import vapor

def smoker():
    """
        before we go see the
        doctor we need to collect
        some basic facts about
        our smoker.
    """
    parser = argparse.ArgumentParser()

    try:
        parser.add_argument('-e',
            help='aws environment',
            type=str, action='store',
            dest='env', required=True)

        parser.add_argument('-i',
            help='instance id',
            type=str, action='store',
            dest='instance_id', required=True)

        parser.add_argument('-s',
            help='aws service with which to instantiate boto3 client, resource, etc',
            type=str, action='store',
            dest='service', required=False, default='ec2')

        parser.add_argument('--version', action='version', version='Nicotine 1.0')

        args = parser.parse_args()
    except Exception as e:
        vapor.vapors('argparsing exception occurred:', e)

    if args.env not in ['dev', 'qa', 'ct', 'pr']:
        vapor.vapors('smoker must be in '
                     'dev, qa, ct, or, pr. Exiting.')
        sys.exit(-1)

    return args

def secret():
    """
        a smoke free smoker
        creates a jira ticket
        for app dev to review
        and this requires jira
        creds
    """
    username = getpass.getuser()
    # needs type and format
    # validation
    password = getpass.getpass('JIRA Password for {}, please:'.format(username))
    secret = {'username': username, 'password': password}
    return secret
