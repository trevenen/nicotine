from clearance import Clearance

from smoker import arg
from doctor import Doctor

# prepepinephrine needs
# to have its methods
# called like a script

def main():
    args = arg()
    doc = Doctor(args.env, args.instance_id, args.service)
    client = doc.create_client()
    resource = doc.create_resource()
    instance = doc.create_instance()
    print(instance.hypervisor)
    clear = Clearance('/Users/me/.aws/credentials', '/usr/local/bin/tool')
    clear.check_fed()
    clear.check_fed_version()

if __name__ == '__main__':
    main()
