import boto3
import datetime
import vapor

from doctors import Doctor

class PrepEpinephrine:
    """
        In rare cases an extreme
        allergic reaction to a nicotine patch occurs and
        server anaphylaxis can occur in the form of kernel
        panics or dependency conflicts (blame app dev
        obviously). If this occurs we must be ready to
        administer a potent dose of Epinephrine to stop
        the reaction at once. In order to administer
        epinephrine we need an AMI on which to rollback:
        clas PrepEpinephrine handles the creation and
        validation of such an AMI.
    """

    def __init__(self, env: str instance_id: str, service: str):
        """
            To prep epinephrine we need to know
            the environment of the smoker,
            their instance_id, the AWS service
            and their attending physician.
        """
        self.env = env
        self.instance_id = instance_id
        self.service = service
        self.doc = Doctor(self.env, self.instance_id, self.service)
        self.client = doc.create_client()
        self.instance = doc.create_instance()

    def create_ami_timestamp(self):
        """
            create a unique timestamp
            for our ami so that it is
            stored as a unique object
            in ec2 AMI
        """
        try:
            self.ami_timestamp = datetime.datetime.utcnow().strftime('%Y%m%d-%s')
            vapors(f"ami_timestamp is: {self.ami_timestamp}")
            return self.ami_timestamp
        except Exception as e:
            vapors('something went wrong with datetime:\n', e)
            raise

    def get_tags(self):
        """ get smoker tags """
        try:
            response = self.client.describe_tags(
                    Filters=[
                                {
                                    'Name': 'resource-id',
                                    'Values': [self.instance_id],
                                },
                            ],
                        )
            self.tags = response['Tags']
            vapors(f"describe_tags response: {response}")
            return self.tags
        except Exception as e:
            vapors('describe_tags error:\n', e)
            raise

    def check_name(self, tg: dict):
        """
            We have to be certain
            who this person is.  Can't
            just be administering epinephrine
            to anyone now can we...
        """
        self.tg = tg

        try:
            self.name = [self.tg.get('Value') for tag in self.tg if tag.get('Key') == 'Name']
            self.smoker_name = name[0]
            vapors(f'smoker name is: {self.smoker_name}')
            return self.smoker_name
        except IndexError as e:
            vapors(f'smoker with instance_id {self.instance_id} ' + \
                   'has no name which is strange. exiting', e)
            raise

    def ami_name(self, nm: str, tm_stamp: str):
        """
            create AMI with a unique name
        """
        self.nm = nm
        self.tm_stamp = tm_stamp
        try:
            self.ami_nm = f'nicotine_patch_{self.nm}_{self.tm_stamp}'
            vapor(f'ami name: {self.ami_nm}')
            return self.ami_nm
        except Exception as e:
            vapors('something went wrong ' + \
                   f'when creating the ami name {self.ami_name}.\n', e)
            raise

    def create_ami(self, nm: str):
        """
            create an AMI in case
            epinephrine needs to be
            aministered
        """
        self.nm = nm
        try:
            response = self.client.create_image(
                Description=self.nm,
                Name=self.nm,
                InstanceId=self.instance_id,
                NoReboot=True)

            self.ami_id= response['ImageId']
            vapors(f'ami {self.nm} has ami id ' + \
                   f'{self.ami_id}. ami creation attempt ' + \
                   f'is below:\n' + \
                   f'{self.nmresponse}')
            return self.ami_id
        except Exception as e:
            vapors('something went wrong ' + \
                   f'when creating ami {self.nm}:\n', e)
            raise

    def test_ami(self, ami_nm: str, ami_id: str):
        """
            confirm epinephrine is
            actually available. Exit in 4
            hours or less if it is anything but.
        """
        self.ami_nm = ami_nm
        self.ami_id = ami_id
        for idx, val in enumerate(range(49)):
            self.ami_state = self.client.describe_images(ImageIds=[self.ami_id])['Images'][0]['State']
            if self.ami_state == 'available':
                vapor.vapors(f'ami {self.ami_nm} with ami id {self.ami_id} ' + \
                             'is available for epinephrine.')
                break
            elif self.ami_state == 'pending':
                if val == 48:
                    vapor.vapors(f'ami {self.ami_nm} with ami id {self.ami_id} ' + \
                                 'unable to form in 4 hours. If you think this ami' + \
                                 'could just take that long then maybe investigate. ' + \
                                 'exiting.')
                    sys.exit(-1)
                else:
                    vapor.vapors(f'ami {self.ami_nm} with ami id {self.ami_id} still forming. sleeping 5 minutes.')
                    time.sleep(300)
            else:
                vapor.vapors(f'ami state is {self.ami_state}. exiting')
                sys.exit(-1)
