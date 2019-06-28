import vapor
import subprocess
import sys

from packaging import version
from pathlib import Path

# medical clearance
# for nicotine patching

class Clearance:

    def __init__(self, creds, tool):
        self.creds = creds
        self.tool = tool

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
            vapor.vapors('cannot find aws credentials file at specified location. ' + \
                         'quick start for credentials setup: ' + \
                         f'{aws_link}\n' + \
                         'exiting.')
            sys.exit(-1)

    def check_tool(self):
        tool_link = 'need tool link'
        tool_path = Path(self.tool)
        if Path.exists(tool_path):
            vapor.vapors('tool binary exists at given location. checking version.')
        else:
            vapor.vapors('cannot find tool binary specified location. ' + \
                         'quick start for tool setup: ' + \
                         f'{tool_link}\n' + \
                         'exiting.')
            sys.exit(-1)

    def check_tool_version(self):
        tool_link = 'need tool link'
        tool_version = '0.0.6'
        tool_version_stdout = subprocess.run([self.tool, '--version'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        current_tool_version = tool_version_stdout[12:17]

        if version.parse(current_tool_version) >= version.parse(tool_version):
            vapor.vapors(f'tool binary version is {current_tool_version} which works. continuing.')
        else:
            vapor.vapors(f'current tool version is {current_tool_version} ' + \
                           f'which is too old. tool version must be at least {tool_version} ' + \
                           f'quick start for upgrading tool below: ' + \
                           f'{tool_link}\n' + \
                           'exiting.')
            sys.exit(-1)
