'''
Client side of the Playnetmano_rm RPC API.
'''

from oslo_config import cfg
from oslo_log import log as logging

from playnetmano_rm.common import config
from playnetmano_rm.common import consts
from playnetmano_rm.common import messaging

CONF = cfg.CONF
LOG = logging.getLogger(__name__)
config.register_options()


class EngineClient(object):
    """Client side of the playnetmano_rm engine rpc API.

    Version History:
     1.0 - Initial version (Mitaka 1.0 release)
    """

    BASE_RPC_API_VERSION = '1.0'

    def __init__(self):
        self._client = messaging.get_rpc_client(
            topic=consts.TOPIC_PLRM_ENGINE,
            server=CONF.host,
            version=self.BASE_RPC_API_VERSION)

    @staticmethod
    def make_msg(method, **kwargs):
        return method, kwargs

    def call(self, ctxt, msg, version=None):
        method, kwargs = msg
        if version is not None:
            client = self._client.prepare(version=version)
        else:
            client = self._client
        return client.call(ctxt, method, **kwargs)

    def cast(self, ctxt, msg, version=None):
        method, kwargs = msg
        if version is not None:
            client = self._client.prepare(version=version)
        else:
            client = self._client
        return client.cast(ctxt, method, **kwargs)

    def get_total_usage_for_tenant(self, ctxt, project_id):
        return self.call(ctxt, self.make_msg('get_total_usage_for_tenant',
                                             project_id=project_id))

    def quota_sync_for_project(self, ctxt, project_id):
        return self.cast(ctxt, self.make_msg('quota_sync_for_project',
                                             project_id=project_id))
