import boto3
import sys
import vapor

from doctor import Doctor

# would be nice to abstract
# the vapors message

class NicotinePatch:
    """
        NicotinePatch is a glorified
        'sudo yum update -y' and
        'sudo shutdown -r now', but it
        executes these commands with intelligence
        and automated instance rollback
    """
    def __init__(self, env: str, instance_id: str,
                 client: Doctor, instance: Doctor,
                 service: str = 'ec2'):
        self.env = env
        self.instance_id = instance_id
        self.client = client
        self.instance = instance
        self.service = service

    def patch(self, patch_command='sudo yum update -y'):
        """
            apply nicotine patch
            via ssm and fail for
            any exception (until exception
            awareness can be improved)
        """
        self.patch_command = patch_command
        try:
            response = self.client.send_command(
                InstanceIds=[self.instance_id],
                DocumentName="sudo_yum_update",
                Parameters={'commands':[self.patch_command]},)
            # command needs some time
            # to complete
            # before checking command id
            time.sleep(60)
            self.command_id = response['Command']['CommandId']
            vapor.vapors(f'patch command {self.patch_command} with'
                         f'command id {self.command_id} for instance '
                         f'{self.instance_id} in env {self.env} '
                         'executed. response below:\n'
                         f'{response}')
            vapor.vapors(f'\n{self.patch_command}')
        except Exception as e:
            vapor.vapors('an exception was thrown during patch attempt'
                         f'for command: {self.patch_command} with command id'
                         f'{self.command_id} for instance '
                         f'{self.instance_id} in env {self.env}. '
                         'exiting; response below:\n'
                         f'{response}', e)
            raise

    def allergy_test(self, cmd_id):
        """
            test if the patch has completed
            in 10 minutes or less. if so: reboot, else:
            fail and rollback via GoodIntentions class.
        """

        try:
            for idx, val in enumerate(range(11)):
                response = self.client.get_command_invocation(
                    InstanceId=self.instance_id,
                    CommandId=self.cmd_id)

                if response['Status'] == 'Success':
                    vapor.vapors(f'patch command {self.patch_command} with command id '
                                 f'{self.cmd_id} for instance '
                                 f'{self.instance_id} in env {self.env} '
                                 'succeeded. response below:\n'
                                 f'{repsonse}')
                    return 0
                elif response['Status'] in ['Delayed', 'InProgress', 'Pending']:
                    if val == 10:
                        vapor.vapors(f'{self.patch_command} with command id'
                                     f'{self.cmd_id} for instance '
                                     f'{self.instance_id} in env {self.env} '
                                     f'has taken 10 minutes to attempt '
                                     f'command execution. rolling back. '
                                     'failed response below:\n'
                                     f'{response}')
                        # launch epinephrine box from prep epinephrine ami
                        # if elb is relevant, roll that machine in behind elb
                        # stop or force stop jacked box
                        # if elb is relevant, roll jacked box out from behind elb
                        # system test new box
                        sys.exit(-1)
                    else:
                        vapor.vapors(f'patch command {self.patch_command} with command id '
                                     f'{self.cmd_id} for instance '
                                     f'{self.instance_id} in env {self.env} has a status of '
                                     f"{response['Status']}. sleeping for 60 seconds "
                                      'and then checking status again.')
                        time.sleep(60)
                        continue

    def anaphylaxis_check(self, name: str, status_code: int, reboot_command='sudo shutdown -r now'):
        self.name = name
        self.reboot_command = reboot_command
        self.status_code = status_code

        # right now the only status_code
        # is zero
        if self.status_code == 0:
            try:
                response = self.client.send_command(
                    InstanceIds=[self.instance_id],
                    DocumentName="sudo_shutdown_now_r",
                    Parameters={'commands':[self.reboot_command]},)

                    vapor.vapors(f'reboot of {self.name} attempted. '
                                 'response below:\n{response}')
            except as Exception e:
                    vapor.vapors('something went wrong when trying to '
                                 f'reboot {self.name}. exception below:\n', e)
                    raise
        else:
            vapor.vapors('anaphylaxis_check method received a status_code '
                         'of {self.status_code} and cannot continue. response is '
                         'below. exiting.')
                    sys.exit(-1)

        # nice case for recursion
        for idx,val in enumerate(range(11)):
            # {'Code': 16, 'Name': 'running'}
            if self.instance.state == 16:
                vapor.vapors(f'reboot of {self.name} successful. system '
                             'testing will now proceed.')
                break
            # {'Code': 0, 'Name': 'pending'}
            elif self.instance.state == 0:
                if val == 10:
                    vapor.vapors(f'reboot of {self.name} has taken '
                                 '10 minutes. exiting.')
                    sys.exit(-1)
            else:
                vapor.vapors(f'reboot attempt of {self.name}'
                             f'has status code of {self.instance.state}.'
                             f'exiting.')
                sys.exit(-1)
