#!/usr/bin/python
# has to be a full import due to Ansible 2.0 compatibility
from ansible.module_utils.basic import *
from waldur_client import WaldurClient, WaldurClientException

DOCUMENTATION = '''
---
module: waldur_os_get_instance
short_description: Get existing OpenStack instance
version_added: 0.1
description:
  - Get an OpenStack instance
requirements:
  - python = 2.7
  - requests
  - python-waldur-client
options:
  access_token:
    description:
      - An access token which has permissions to create an OpenStack instances.
    required: true
  api_url:
    description:
      - Fully qualified url to the Waldur.
    required: true
  name:
    description:
      - The name or UUID of existing OpenStack instance.
    required: true
  project:
    description:
      - The name or id of the project to add an instance to.
    required: true
'''

EXAMPLES = '''
- name: Get an OpenStack instance
  hosts: localhost
  tasks:
    - name: add instance
      waldur_os_get_instance:
        access_token: b83557fd8e2066e98f27dee8f3b3433cdc4183ce
        api_url: https://waldur.example.com:8000/api
        name: Warehouse instance
        project: OpenStack Project
'''


def main():
    fields = {
        'api_url': {'required': True, 'type': 'str'},
        'access_token': {'required': True, 'type': 'str'},
        'name': {'required': True, 'type': 'str'},
        'project': {'required': False, 'type': 'str'},
    }
    module = AnsibleModule(argument_spec=fields)

    client = WaldurClient(module.params['api_url'], module.params['access_token'])
    try:
        instance = client.get_instance(
            name=module.params['name'],
            project=module.params['project'],
        )
    except WaldurClientException as error:
        module.fail_json(msg=error.message)
    else:
        module.exit_json(instance=instance)


if __name__ == '__main__':
    main()
