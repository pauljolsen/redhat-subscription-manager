#!/usr/bin/python


from ansible.module_utils.basic import AnsibleModule, json
from ansible.module_utils.urls import open_url, urllib_request


class RedHatSubscription(object):

    def __init__(self, token):
        self.token = token
        self.access_token = self.get_access()
        self.headers = {
            "Authorization": "Bearer {}".format(self.access_token)
        }

    def get_access(self):
        access = open_url(
            url="https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token",
            method='POST',
            data="grant_type=refresh_token&client_id=rhsm-api&refresh_token={}".format(self.token)
        )
        if access.status != 200:
            return False
        return json.loads(access.read())['access_token']

    def get_systems(self, offset=0, limit=100):
        systems = open_url(
            url="https://api.access.redhat.com/management/v1/systems?limit={}&offset={}".format(limit, offset),
            method='GET',
            headers=self.headers,
        )
        return json.loads(systems.read())

    def system_uuid(self, name, offset=0, limit=100):

        systems = self.get_systems(offset=offset, limit=limit)

        # If we find the system, return the UUID
        for system in systems['body']:
            if system['name'] == name:
                return system['uuid']

        # If we don't find it, and this is the last page, we're done
        if systems['pagination']['count'] < limit:
            return None

        # But otherwise we need to get the next page of results and check
        else:
            return self.system_uuid(name, offset=offset+limit, limit=limit)

    def delete_system(self, uuid):
        deleted = open_url(
            url='https://api.access.redhat.com/management/v1/systems/{}'.format(uuid),
            method='DELETE',
            headers=self.headers,
        )
        if deleted.status != 204:
            return False
        return True


def main():

    argument_spec = dict(
        token=dict(type='str', required=True, no_log=True),
        hostname=dict(type='str', required=True)
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False
    )
    try:
        r = RedHatSubscription(module.params.get("token"))
        uuid = r.system_uuid(module.params.get("hostname"))
        if not uuid:
            module.exit_json(changed=False, meta={"msg": "Could not find system."})
        deleted = r.delete_system(uuid)
        if deleted:
            module.exit_json(changed=True, meta={"msg": "System deleted."})
        else:
            module.fail_json(meta={"msg": "The system exists, but something went wrong deleting it."})

    except urllib_request.HTTPError as e:
        module.fail_json(msg=json.loads(e.fp.read()))

    except:
        module.fail_json(meta={"msg": "Unknown error."})


if __name__ == '__main__':
    main()
