#!/usr/bin/env python

"""
Playnetmano_rm Engine Server.
"""

import eventlet
eventlet.monkey_patch()

from oslo_config import cfg
from oslo_i18n import _lazy
from oslo_log import log as logging
from oslo_service import service

from playnetmano_rm.common import config
from playnetmano_rm.common import consts
from playnetmano_rm.common import messaging

_lazy.enable_lazy()
config.register_options()
LOG = logging.getLogger('playnetmano_rm.engine')


def main():
    logging.register_options(cfg.CONF)
    cfg.CONF(project='playnetmano_rm', prog='playnetmano_rm-engine')
    logging.setup(cfg.CONF, 'playnetmano_rm-engine')
    logging.set_defaults()
    messaging.setup()

    from playnetmano_rm.engine import service as engine

    # the service that you would like to start and must be instance of service base (oslo_service.service.ServiceBase)
    srv = engine.EngineService(cfg.CONF.host,
                               consts.TOPIC_PLRM_ENGINE)
    # details could refer to this link(http://docs.openstack.org/developer/oslo.service/api/service.html)
    launcher = service.launch(cfg.CONF,
                              srv, workers=cfg.CONF.workers)
    # the following periodic tasks are intended serve as HA checking
    # srv.create_periodic_tasks()
    launcher.wait()

if __name__ == '__main__':
    main()
