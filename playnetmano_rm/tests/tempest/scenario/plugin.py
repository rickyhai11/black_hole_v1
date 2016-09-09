
import os

from tempest.test_discover import plugins

from playnetmano_rm.tests.tempest.scenario import config as plrm_config


class Playnetmano_rmTempestPlugin(plugins.TempestPlugin):
    def load_tests(self):
        base_path = os.path.split(os.path.dirname(
            os.path.abspath(__file__)))[0]
        test_dir = 'scenario'
        full_test_dir = os.path.join(base_path, test_dir)
        return full_test_dir, base_path

    def register_opts(self, conf):
        # additional options for playnetmano_rm
        conf.register_group(plrm_config.kb_group)
        conf.register_opts(plrm_config.KBGroup, group='playnetmano_rm')
        conf.register_opt(plrm_config.service_option,
                          group='service_available')

    def get_opt_lists(self):
        return [('playnetmano_rm', plrm_config.KBGroup),
                ('service_available', [plrm_config.service_option])]
