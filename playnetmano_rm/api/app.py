import pecan

from keystonemiddleware import auth_token
from oslo_config import cfg
from oslo_middleware import request_id
from oslo_service import service

from playnetmano_rm.common import exceptions as k_exc
from playnetmano_rm.common.i18n import _


def setup_app(*args, **kwargs):
    config = {
        'server': {
            'port': cfg.CONF.bind_port,
            'host': cfg.CONF.bind_host
        },
        'app': {
            'root': 'playnetmano_rm.api.controllers.root.RootController',
            'modules': ['playnetmano_rm.api'],
            'errors': {
                400: '/error',
                '__force_dict__': True
            }
        }
    }
    pecan_config = pecan.configuration.conf_from_dict(config)

    # app_hooks = [], hook collection will be put here later

    app = pecan.make_app(
        pecan_config.app.root,
        debug=False,
        wrap_app=_wrap_app,
        force_canonical=False,
        hooks=[],
        guess_content_type_from_ext=True
    )

    return app


def _wrap_app(app):
    app = request_id.RequestId(app)

    if cfg.CONF.auth_strategy == 'noauth':
        pass
    elif cfg.CONF.auth_strategy == 'keystone':
        app = auth_token.AuthProtocol(app, {})
    else:
        raise k_exc.InvalidConfigurationOption(
            opt_name='auth_strategy', opt_value=cfg.CONF.auth_strategy)

    return app


_launcher = None


def serve(api_service, conf, workers=1):
    global _launcher
    if _launcher:
        raise RuntimeError(_('serve() can only be called once'))

    _launcher = service.launch(conf, api_service, workers=workers)


def wait():
    _launcher.wait()
