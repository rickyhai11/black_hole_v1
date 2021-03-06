'''
Entry point for the application. It should be start from here
'''

import pecan

from playnetmano_rm.api.controllers import quota_manager
from playnetmano_rm.api.controllers.v1 import quota_class


class RootController(object):

    @pecan.expose('json')
    def _lookup(self, version, *remainder):
        if version == 'v1.0':
            return V1Controller(), remainder

    @pecan.expose(generic=True, template='json')
    def index(self):
        return {
            "versions": [
                {
                    "status": "CURRENT",
                    "links": [
                        {
                            "rel": "self",
                            "href": pecan.request.application_url + "/v1.0/"
                            }
                        ],
                    "id": "v1.0",
                    "updated": "2016-08-20"
                    }
                ]
            }

    @index.when(method='POST')
    @index.when(method='PUT')
    @index.when(method='DELETE')
    @index.when(method='HEAD')
    @index.when(method='PATCH')
    def not_supported(self):
        pecan.abort(405)


class V1Controller(object):

    def __init__(self):

        self.sub_controllers = {
            "os-quota-sets": quota_manager.QuotaManagerController,
            "os-quota-class-sets": quota_class.QuotaClassSetController,
        }

        for name, ctrl in self.sub_controllers.items():
            setattr(self, name, ctrl)

    def _get_resource_controller(self, tenant_id, remainder):
        if not remainder:
            pecan.abort(404)
            return
        resource = remainder[0]
        if resource not in self.sub_controllers:
            pecan.abort(404)
            return

        return self.sub_controllers[resource](), remainder[1:]

    @pecan.expose()
    def _lookup(self, tenant_id, *remainder):
        return self._get_resource_controller(tenant_id, remainder)

    @pecan.expose(generic=True, template='json')
    def index(self):
        return {
            "version": "1.0",
            "links": [
                {"rel": "self",
                 "href": pecan.request.application_url + "/v1.0"}
            ] + [
                {"rel": name,
                 "href": pecan.request.application_url +
                    "/v1.0/{tenant_id}/" + name}
                for name in sorted(self.sub_controllers)
            ]
        }

    @index.when(method='POST')
    @index.when(method='PUT')
    @index.when(method='DELETE')
    @index.when(method='HEAD')
    @index.when(method='PATCH')
    def not_supported(self):
        pecan.abort(405)
