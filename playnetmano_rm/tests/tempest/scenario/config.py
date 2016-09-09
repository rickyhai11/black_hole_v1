"""Configurations for playnetmano_rm Tempest Plugin."""

from oslo_config import cfg
from tempest import config  # noqa

service_option = cfg.BoolOpt('playnetmano_rm',
                             default=True,
                             help="Whether or not playnetmano_rm is expected to be "
                                  "available")

kb_group = cfg.OptGroup(
    name="playnetmano_rm",
    title="playnetmano_rm configuration options")

KBGroup = [
    cfg.StrOpt(name='endpoint_type',
               default='publicURL',
               help="Endpoint type of playnetmano_rm service."),
    cfg.IntOpt(name='TIME_TO_SYNC',
               default=30,
               help="Maximum time to wait for a sync call to complete."),
    cfg.StrOpt(name='endpoint_url',
               default='http://127.0.0.1:8118/',
               help="Endpoint URL of playnetmano_rm service."),
    cfg.StrOpt(name='api_version',
               default='v1.0',
               help="Api version of playnetmano_rm service.")
]
