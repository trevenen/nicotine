import vapor
import subprocess
import sys

from packaging import version
from pathlib import Path

# medical clearance
# for nicotine patching

class Clearance:

    def __init__(self, creds, fed):
        self.creds = creds
        self.fed = fed

    def check_botocore(self):
        try:
            from botocore.exceptions import ClientError
            from botocore.config import Config
            vapor.vapors('botocore module found; checking boto3 module next.')
        except ImportError as e:
            vapor.vapors('Cannot find botocore module for import. Exiting', e)
            raise

    def check_boto3(self):
        try:
            import boto3
            vapor.vapors('boto3 module found; checking aws credentials file next.')
        except ImportError as e:
            vapor.vapors('Cannot find boto3 module for import. Exiting.', e)
            raise

    def check_credentials(self):
        aws_link = 'https://docs.aws.amazon.com/sdk-for-php/v3/developer-guide/guide_credentials_profiles.html'
        creds_path = Path(self.creds)
        if Path.exists(creds_path):
            vapor.vapors('aws credentials file exists at given location. checking version.')
        else:
            vapor.vapors('cannot find aws credentials file at specified location. '
                         'quick start for credentials setup: '
                         f'{aws_link}\n'
                         'exiting.')
            sys.exit(-1)

    def check_fed(self):
        fed_link = 'need fed link'
        fed_path = Path(self.fed)
        if Path.exists(fed_path):
            vapor.vapors('fed binary exists at given location. checking version.')
        else:
            vapor.vapors('cannot find fed binary specified location. '
                         'quick start for fed setup: '
                         f'{fed_link}\n'
                         'exiting.')
            sys.exit(-1)

    def check_fed_version(self):
        fed_link = 'need fed link'
        fed_version = '0.0.6'
        fed_version_stdout = subprocess.run([self.fed, '--version'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        current_fed_version = fed_version_stdout[12:17]

        if version.parse(current_fed_version) >= version.parse(fed_version):
            vapor.vapors(f'fed binary version is {current_fed_version} which works. continuing.')
        else:
            vapor.vapors(f'current fed version is {current_fed_version} '
                           f'which is too old. fed version must be at least {fed_version} '
                           f'quick start for upgrading fed below: '
                           f'{fed_link}\n'
                           'exiting.')
            sys.exit(-1)
