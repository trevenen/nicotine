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
    def __init__(self, env, instance_id, service):
        self.env = env
        self.instance_id = instance_id
        self.service = service
        doc = Doctor(self, self.env, self.instance_id, self.service)
        client = doc.create_client()
        instance = doc.create_instance()

    def patch(self, patch_command='sudo yum update -y'):
        """
            apply nicotine patch
            via ssm and fail for
            any exception (until exception
            awareness can be improved)
        """
        self.patch_command = patch_command
        try:
            response = client.send_command(
                InstanceIds=[self.instance_id],
                DocumentName="sudo_yum_update",
                Parameters={'commands':[self.patch_command]},)
            # command needs some time
            # to complete
            # before checking command id
            time.sleep(60)
            self.command_id = response['Command']['CommandId']
            vapor.vapors(f'patch command {self.patch_command} with' + \
                         f'command id {self.command_id} for instance ' + \
                         f'{self.instance_id} in env {self.env} ' + \
                         'executed. response below:\n' + \
                         f'{response}')
            vapor.vapors(f'\n{self.patch_command}')
        except Exception as e:
            vapor.vapors('an exception was thrown during patch attempt' + \
                         f'for command: {self.patch_command} with command id' + \
                         f'{self.command_id} for instance ' + \
                         f'{self.instance_id} in env {self.env}. ' + \
                         'exiting; response below:\n' + \
                         f'{response}', e)

    def allergy_test(self, self.cmd_id):
        """
            test if the patch has completed
            in 10 minutes or less. if so: reboot, else:
            fail and rollback via GoodIntentions class.
        """

        try:
            for idx, val in enumerate(range(11)):
                response = client.get_command_invocation(
                    InstanceId=self.instance_id,
                    CommandId=self.cmd_id)

                if response['Status'] == 'Success':
                    vapor.vapors(f'patch command {self.patch_command} with command id ' + \
                                 f'{self.cmd_id} for instance ' + \
                                 f'{self.instance_id} in env {self.env} ' + \
                                 'succeeded. response below:\n'
                                 f'{repsonse})
                    return 0
                elif response['Status'] in ['Delayed', 'InProgress', 'Pending']:
                    if val == 10:
                        vapor.vapors(f'{self.patch_command} with command id' + \
                                     f'{self.cmd_id} for instance ' + \
                                     f'{self.instance_id} in env {self.env} ' + \
                                     f'has taken 10 minutes to attempt ' + \
                                     f'command execution. rolling back. ' + \
                                     'failed response below:\n'
                                     f'{response}')
                        # launch epinephrine box from prep epinephrine ami
                        # if elb is relevant, roll that machine in behind elb
                        # stop or force stop jacked box
                        # if elb is relevant, roll jacked box out from behind elb
                        # system test new box
                        sys.exit(-1)
                    else:
                        vapor.vapors(f'patch command {self.patch_command} with command id ' + \
                                     f'{self.cmd_id} for instance ' + \
                                     f'{self.instance_id} in env {self.env} has a status of ' + \
                                     f'{response['Status']}. sleeping for 60 seconds ' + \
                                      'and then checking status again.')
                        time.sleep(60)

    def anaphylaxis_check(self, name, reboot_command='sudo shutdown -r now', status_code: int):
        self.name = name
        self.reboot_command = reboot_command
        self.status_code = status_code

        # status success 
        #     break
        # status pending
        #     val == limit
        #         something
        # status not success and not pending
        #     exit/possibly something
        #
        # ^ status(self, status, limit, attempts, action=[start, stop], force=[true, false])
        # anaphylaxis algo
        #   attempt reboot
        #       status success
        #           system test 
        #       status pending
        #           val == limit
        #               attempt force stop
        #           else
        #               continue
        #                   status success
        #                       system test
        #                   status pending
        #                       val == limit
        #                           force stop
        #                               attempt force stop
        #                                   status success
        #                                       attempt start
        #                                   status pending
        #                                       if val == limit
        #                                           sys.exit(-1)
        #                                   status not success and not pending
        #                                       sys.exit(-1)
        #       status not success and not pending
        #           sys.exit(-1)
        #                   val != limit
        #                       check again
        #       status not success and not pending
        #           sys.exit(-1)

        # right now the only status_code
        # is zero
        if self.status_code == 0:
            try:
                response = client.send_command(
                    InstanceIds=[self.instance_id],
                    DocumentName="sudo_shutdown_now_r",
                    Parameters={'commands':[self.reboot_command]},)

                    vapor.vapors(f'reboot of {self.name} attempted. ' + \
                                 'response below:\n{response}')
            except as Exception e:
                    vapor.vapors('something went wrong when trying to ' + \
                                 f'reboot {self.name}. exception below:\n', e)
                    sys.exit(-1)
        else:
            vapor.vapors('anaphylaxis_check method received a status_code ' + \
                         'of {self.status_code} and cannot continue. response is ' + \
                         'below. exiting.')
                    sys.exit(-1)


        # nice case for recursion
        for idx,val in enumerate(range(11)):
            # {'Code': 16, 'Name': 'running'}
            if instance.state == 16:
                vapor.vapors(f'reboot of {self.name} successful. system ' + \
                             'testing will now proceed.')
                break
            # {'Code': 0, 'Name': 'pending'}
            elif instance.state == 0:
                if val == 10:
                    vapor.vapors(f'reboot of {self.name} has taken ' + \
                                 '10 minutes: attempting force reboot.')
                    try:
                        response = client.stop_instances(
                            InstanceIds=[self.instance_id],
                            Force=True, DryRun=False,
                            Hibernate=False)
                        vapor.vapors(f'attemping force stop of {self.name}. ' + \
                                     f'reponse below.\n{response}')
                        for idx,val in enumerate(range(6)):
                            # {'Code': 80, 'Name': 'stopped'}
                            if instance.state == 80:
                                vapor.vapors(f'force stop of {self.name} successful. going ' + \
                                             'to attempt start now.')
                                try:
                                    response = client.start_instances(InstanceIds=[self.instance_id], DryRun=False)
                                    vapor.vapors('attempting start of {self.name}.' + \
                                                 f'response below:\n{response}')
                                    for idx,val in enumerate(range(4)):
                                        # {'Code': 80, 'Name': 'stopped'}
                                        if instance.state == 16:
                                            vapor.vapors(f'start of {self.name} successful. ' + \
                                                         'system testing will now being.')
                                            break
                                        # {'Code': 0, 'Name': 'pending'}
                                        elif instance.state == 0:
                                            if val == 5:
                                                vapor.vapors(f'start of {self.name} has taken ' + \
                                                             '5 minutes: something is likely wrong.
                                                             'exiting.')
                                                sys.exit(-1)
                                        else:
                                            vapor.vapors(f'start attempt of {self.name}' + \
                                                         f'has status code of {instance.state}.' + \
                                                         f'exiting.')
                                            sys.exit(-1)
                                except Exception as e:
                                    vapor.vapors('something went wrong with attempted start ' + \
                                                 f'of {self.name}. exiting', e)
                                    sys.exit(-1)
                                break
                            # {'Code': 0, 'Name': 'pending'}
                            elif instance.state == 0:
                                if val == 10:
                                    vapor.vapors(f'reboot of {self.name} has taken ' + \
                                                 '10 minutes: attempting force reboot.')
                    except Exception as e:
                        vapor.vapors('something went wrong when attempting ' + \
                                     f'force stop of {self.name}. error below:\n.', e)
                        sys.exit(-1)
            else:
                vapor.vapors(f'start attempt of {self.name}' + \
                             f'has status code of {instance.state}.' + \
                             f'exiting.')
                sys.exit(-1)
