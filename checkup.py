import boto3
import sys
import vapor

from doctor import Doctor

class Checkup:
    """
        Checkup runs system tests.
        Inherit Checkup to implement
        system tests for any stack
        you like.
    """
    def __init__(self, env: str, instance_id: str,
                 service: str, client: Doctor):
        self.env = env
        self.instance_id = instance_id
        self.service = service
        self.client = client

    def checkup(self, command='sudo /etc/init.d/tomcat8 status'):
        """
            Check takes a command, attempts
            it and fails if it doesn't
            have a 'Success' status in time.
            Nicotine defaults to testing tomcat
            because we have historically been a
            java shop.
        """
        self.command = command
        try:
            response = self.client.send_command(
                InstanceIds=[self.instance_id],
                DocumentName=self.command,
                Parameters={'commands':[self.command]},)
            # command needs some time
            # to complete
            # before checking command id
            time.sleep(60)
            self.command_id = response['Command']['CommandId']
            vapor.vapors(f'command {self.command} with'
                         f'command id {self.command_id} for instance '
                         f'{self.instance_id} in env {self.env} '
                         'executed. response below:\n'
                         f'{response}')
            return self.command_id
        except Exception as e:
            vapor.vapors('an exception was thrown during patch attempt'
                         f'for command: {self.command} with command id'
                         f'{self.command_id} for instance '
                         f'{self.instance_id} in env {self.env}. '
                         'exiting; response below:\n'
                         f'{response}', e)
            raise

    def checkup_satisfaction(self, self.cmd_id):
        """
            test if the checkup command has completed
            in 2 minutes or less. if so: run next
            command or exit.
        """

        try:
            for idx, val in enumerate(range(3)):
                response = self.client.get_command_invocation(
                    InstanceId=self.instance_id,
                    CommandId=self.cmd_id)

                if response['Status'] == 'Success':
                    vapor.vapors(f'command {self.command} with command id '
                                 f'{self.cmd_id} for instance '
                                 f'{self.instance_id} in env {self.env} '
                                 'succeeded. smoke_free!!! (creating jira ticket)')
                    return 0
                elif response['Status'] in ['Delayed', 'InProgress', 'Pending']:
                    if val == 2:
                        vapor.vapors(f'{self.command} with command id'
                                     f'{self.cmd_id} for instance '
                                     f'{self.instance_id} in env {self.env} '
                                     f'has taken 2 minutes to attempt '
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
                        vapor.vapors(f'command {self.command} with command id '
                                     f'{self.cmd_id} for instance '
                                     f'{self.instance_id} in env {self.env} has a status of '
                                     f'{response['Status']}. sleeping for 60 seconds '
                                      'and then checking status again.')
                        time.sleep(60)
