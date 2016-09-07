"""
CLI interface for playnetmano_rm management.
"""

import sys

from oslo_config import cfg
from oslo_log import log as logging

from playnetmano_rm.common import config
from playnetmano_rm.db import api
from playnetmano_rm import version

config.register_options()
CONF = cfg.CONF


def do_db_version():
    '''Print database's current migration level.'''
    print(api.db_version(api.get_engine()))


def do_db_sync():
    '''Place a database under migration control and upgrade.

    DB is created first if necessary.
    '''
    api.db_sync(api.get_engine(), CONF.command.version)


def add_command_parsers(subparsers):
    parser = subparsers.add_parser('db_version')
    parser.set_defaults(func=do_db_version)

    parser = subparsers.add_parser('db_sync')
    parser.set_defaults(func=do_db_sync)
    parser.add_argument('version', nargs='?')
    parser.add_argument('current_version', nargs='?')

command_opt = cfg.SubCommandOpt('command',
                                title='Commands',
                                help='Show available commands.',
                                handler=add_command_parsers)


def main():
    logging.register_options(CONF)
    logging.setup(CONF, 'playnetmano_rm-manage')
    CONF.register_cli_opt(command_opt)

    try:
        default_config_files = cfg.find_config_files('playnetmano_rm',
                                                     'playnetmano_rm-engine')
        CONF(sys.argv[1:], project='playnetmano_rm', prog='playnetmano_rm-manage',
             version=version.version_info.version_string(),
             default_config_files=default_config_files)
    except RuntimeError as e:
        sys.exit("ERROR: %s" % e)

    try:
        CONF.command.func()
    except Exception as e:
        sys.exit("ERROR: %s" % e)

if __name__ == '__main__':
    main()
