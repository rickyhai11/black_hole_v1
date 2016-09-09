import collections
import time

from tempest import config
from tempest.lib.common import api_version_utils
from tempest.lib.common.utils import data_utils
import tempest.test

from playnetmano_rm.tests.tempest.scenario import consts
from playnetmano_rm.tests.tempest.scenario.quota_management \
    import sync_client

CONF = config.CONF
GLOBAL_INSTANCE_LIMIT = 10
GLOBAL_NETWORK_LIMIT = 10
GLOBAL_VOLUME_LIMIT = 10
DEFAULT_QUOTAS = consts.DEFAULT_QUOTAS
# Time to wait for sync to finish
TIME_TO_SYNC = CONF.kingbird.TIME_TO_SYNC


class BasePlaynetmano_rmTest(api_version_utils.BaseMicroversionTest,
                             tempest.test.BaseTestCase):
    """Base test case class for all playnetmano_rm API tests."""

    @classmethod
    def skip_checks(cls):
        super(BasePlaynetmano_rmTest, cls).skip_checks()

    def setUp(self):
        super(BasePlaynetmano_rmTest, self).setUp()

    @classmethod
    def setup_credentials(cls):
        super(BasePlaynetmano_rmTest, cls).setup_credentials()
        session = sync_client.get_session()
        cls.auth_token = session.get_token()
        cls.key_client = sync_client.get_key_client(session)
        cls.regions = sync_client.get_regions(cls.key_client)

    @classmethod
    def setup_clients(cls):
        super(BasePlaynetmano_rmTest, cls).setup_clients()

    @classmethod
    def resource_setup(cls):
        super(BasePlaynetmano_rmTest, cls).resource_setup()
        cls.class_name = data_utils.rand_name('kb-class')

    @classmethod
    def create_resources(cls):
        # Create Project, User, flavor, subnet & network for test
        project_name = data_utils.rand_name('kb-project')
        user_name = data_utils.rand_name('kb-user')
        password = data_utils.rand_name('kb-password')
        cls.openstack_details = sync_client.get_openstack_drivers(
            cls.key_client,
            cls.regions[0],
            project_name,
            user_name,
            password)
        cls.openstack_drivers = cls.openstack_details['os_drivers']
        cls.session = cls.openstack_details['session']
        cls.resource_ids = sync_client.create_resources(cls.openstack_drivers)
        cls.resource_ids.update(cls.openstack_details)
        cls.resource_ids["server_ids"] = []
        cls.session = cls.openstack_details['session']

    @classmethod
    def resource_cleanup(cls):
        super(BasePlaynetmano_rmTest, cls).resource_cleanup()

    @classmethod
    def delete_resources(cls):
        sync_client.resource_cleanup(cls.openstack_drivers, cls.resource_ids)

    @classmethod
    def create_custom_playnetmano_rm_quota(cls, project_id, new_quota_values):
        new_values = sync_client.create_custom_playnetmano_rm_quota(
            cls.auth_token, project_id, new_quota_values)
        return new_values

    @classmethod
    def get_custom_playnetmano_rm_quota(cls, project_id):
        return_quotas = sync_client.get_custom_playnetmano_rm_quota(
            cls.auth_token, project_id)
        return return_quotas

    @classmethod
    def delete_custom_playnetmano_rm_quota(cls, project_id, quota_to_delete=None):
        deleted_quotas = sync_client.delete_custom_playnetmano_rm_quota(
            cls.auth_token, project_id, quota_to_delete)
        return deleted_quotas

    @classmethod
    def get_default_playnetmano_rm_quota(cls):
        return_quotas = sync_client.get_default_playnetmano_rm_quota(cls.auth_token)
        return return_quotas

    @classmethod
    def quota_sync_for_project(cls, project_id):
        sync_status = sync_client.quota_sync_for_project(
            cls.auth_token, project_id)
        return sync_status

    @classmethod
    def get_quota_usage_for_project(cls, project_id):
        quota_usage = sync_client.get_quota_usage_for_project(
            cls.auth_token, project_id)
        return quota_usage

    @classmethod
    def create_custom_playnetmano_rm_quota_wrong_token(cls, project_id,
                                                       new_quota_values):
        new_values = sync_client.create_custom_playnetmano_rm_quota_wrong_token(
            cls.auth_token, project_id, new_quota_values)
        return new_values

    @classmethod
    def create_instance(cls, count=1):
        try:
            server_ids = sync_client.create_instance(cls.openstack_drivers,
                                                     cls.resource_ids, count)
        except Exception as e:
            server_ids = list(e.args)
            raise
        finally:
            cls.resource_ids["server_ids"].extend(server_ids)

    @classmethod
    def delete_instance(cls):
        sync_client.delete_instance(cls.openstack_drivers, cls.resource_ids)

    @classmethod
    def calculate_quota_limits(cls, project_id):
        calculated_quota_limits = collections.defaultdict(dict)
        resource_usage = sync_client.get_usage_from_os_client(
            cls.session, cls.regions, project_id)
        total_usages = cls.get_summation(resource_usage)
        for current_region in cls.regions:
            # Calculate new limit for instance count
            global_remaining_limit = GLOBAL_INSTANCE_LIMIT - \
                total_usages['instances']
            instances_limit = global_remaining_limit + resource_usage[
                current_region]['instances']
            # Calculate new limit for network count
            global_remaining_limit = GLOBAL_NETWORK_LIMIT - \
                total_usages['network']
            network_limit = global_remaining_limit + resource_usage[
                current_region]['network']
            # Calculate new limit for volume count
            global_remaining_limit = GLOBAL_VOLUME_LIMIT - \
                total_usages['volumes']
            volume_limit = global_remaining_limit + resource_usage[
                current_region]['volumes']
            calculated_quota_limits.update(
                {current_region: [instances_limit, network_limit,
                                  volume_limit]})
        return calculated_quota_limits

    @classmethod
    def get_summation(cls, regions_dict):
        # Adds resources usages from different regions
        single_region = {}
        resultant_dict = collections.Counter()
        for current_region in regions_dict:
            single_region[current_region] = collections.Counter(
                regions_dict[current_region])
            resultant_dict += single_region[current_region]
        return dict(resultant_dict)

    @classmethod
    def get_usage_manually(cls, project_id):
        resource_usage = sync_client.get_usage_from_os_client(
            cls.session, cls.regions, project_id)
        resource_usage = cls.get_summation(resource_usage)
        return {'quota_set': resource_usage}

    @classmethod
    def get_actual_limits(cls, project_id):
        actual_limits = sync_client.get_actual_limits(
            cls.session, cls.regions, project_id)
        return actual_limits

    @classmethod
    def wait_sometime_for_sync(cls):
        time.sleep(TIME_TO_SYNC)

    @classmethod
    def set_default_quota(cls, project_id, quota_to_set):
        sync_client.set_default_quota(
            cls.session, cls.regions, project_id, **quota_to_set)

    @classmethod
    def update_quota_for_class(cls, class_name, new_quota_values):
        new_values = sync_client.update_quota_for_class(
            cls.auth_token, class_name, new_quota_values)
        return new_values

    @classmethod
    def get_quota_for_class(cls, class_name):
        return_quotas = sync_client.get_quota_for_class(
            cls.auth_token, class_name)
        return return_quotas

    @classmethod
    def delete_quota_for_class(cls, class_name):
        deleted_quotas = sync_client.delete_quota_for_class(
            cls.auth_token, class_name)
        return deleted_quotas
