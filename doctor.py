import boto3

class Doctor:

    """
        Doctors help
        smokers get on the patch
    """

    def __init__(self, env: str, instance_id: str, service: str = 'ec2'):
        self.env = env
        self.instance_id = instance_id
        self.service = service
        self.session = boto3.session.Session(profile_name=self.env)

    def create_client(self):
        self.client = self.session.client(self.service)
        return self.client

    def create_resource(self):
        self.resource = self.session.resource(self.service)
        return self.resource

    def create_instance(self):
        self.instance = self.session.resource(self.service).Instance(self.instance_id)
        return self.instance
