
import sys

import eventlet
from oslo_config import cfg
from oslo_log import log as logging
from oslo_service import systemd
from oslo_service import wsgi

import logging as std_logging

from playnetmano_rm.api import api_config
from playnetmano_rm.api import app

from playnetmano_rm.common import config
from playnetmano_rm.common.i18n import _LI
from playnetmano_rm.common.i18n import _LW
from playnetmano_rm.common import messaging

CONF = cfg.CONF
config.register_options()
LOG = logging.getLogger('playnetmano_rm.api')
eventlet.monkey_patch(os=False)


def main():
    api_config.init(sys.argv[1:])
    api_config.setup_logging()
    application = app.setup_app()

    host = CONF.bind_host
    port = CONF.bind_port
    workers = CONF.api_workers

    if workers < 1:
        LOG.warning(_LW("Wrong worker number, worker = %(workers)s"), workers)
        workers = 1

    LOG.info(_LI("Server on http://%(host)s:%(port)s with %(workers)s"),
             {'host': host, 'port': port, 'workers': workers})
    messaging.setup()
    systemd.notify_once()
    service = wsgi.Server(CONF, "playnetmano_rm", application, host, port)

    app.serve(service, CONF, workers)

    LOG.info(_LI("Configuration:"))
    CONF.log_opt_values(LOG, std_logging.INFO)

    app.wait()


if __name__ == '__main__':
    main()
