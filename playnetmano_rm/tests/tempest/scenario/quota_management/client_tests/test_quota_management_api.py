
from playnetmano_rm.tests.tempest.scenario.quota_management. \
    client_tests import base
from tempest import config

import novaclient

CONF = config.CONF
DEFAULT_QUOTAS = base.DEFAULT_QUOTAS


class Playnetmano_rmQMTestJSON(base.BasePlaynetmano_rmTest):

    @classmethod
    def setup_clients(self):
        super(Playnetmano_rmQMTestJSON, self).setup_clients()

    def tearDown(self):
        super(Playnetmano_rmQMTestJSON, self).tearDown()

    @classmethod
    def resource_cleanup(self):
        super(Playnetmano_rmQMTestJSON, self).resource_cleanup()
        self.delete_resources()

    @classmethod
    def resource_setup(self):
        super(Playnetmano_rmQMTestJSON, self).resource_setup()
        self.create_resources()

    def test_playnetmano_rm_put_method(self):
        new_quota = {"quota_set": {"instances": 15, "cores": 10}}
        actual_value = self.create_custom_playnetmano_rm_quota(
            self.resource_ids["project_id"],
            new_quota)
        expected_value = {
            self.resource_ids["project_id"]: new_quota["quota_set"]
            }
        self.assertEqual(expected_value, eval(actual_value))

    def test_playnetmano_rm_get_method(self):
        new_quota = {"quota_set": {"instances": 15, "cores": 10}}
        self.create_custom_playnetmano_rm_quota(self.resource_ids["project_id"],
                                                new_quota)
        actual_value = self.get_custom_playnetmano_rm_quota(
            self.resource_ids["project_id"])
        new_quota["quota_set"].update(
            {'project_id': self.resource_ids["project_id"]}
            )
        self.assertEqual(new_quota, eval(actual_value))

    def test_playnetmano_rm_delete_method(self):
        new_quota = {"quota_set": {"instances": 15, "cores": 10}}
        quota_to_delete = {"quota_set": ["cores"]}
        self.create_custom_playnetmano_rm_quota(self.resource_ids["project_id"],
                                                new_quota)
        self.delete_custom_playnetmano_rm_quota(self.resource_ids["project_id"],
                                                quota_to_delete)
        quota_after_delete = eval(self.get_custom_playnetmano_rm_quota(
            self.resource_ids["project_id"]))
        self.assertNotIn("cores", quota_after_delete["quota_set"])

    def test_playnetmano_rm_delete_all_method(self):
        new_quota = {"quota_set": {"instances": 15, "cores": 10}}
        self.create_custom_playnetmano_rm_quota(self.resource_ids["project_id"],
                                                new_quota)
        self.delete_custom_playnetmano_rm_quota(self.resource_ids["project_id"])
        actual_quota_after_delete = eval(self.get_custom_playnetmano_rm_quota(
            self.resource_ids["project_id"]))
        expected_quota_after_delete = {
            "quota_set": {
                "project_id": self.resource_ids["project_id"]
                }
            }
        self.assertEqual(expected_quota_after_delete,
                         actual_quota_after_delete)

    def test_playnetmano_rm_get_default_method_after_update(self):
        new_quota = {"quota_set": {"instances": 15, "cores": 10}}
        self.create_custom_playnetmano_rm_quota(self.resource_ids["project_id"],
                                                new_quota)
        actual_value = self.get_default_playnetmano_rm_quota()
        if 'id' in DEFAULT_QUOTAS['quota_set']:
            del DEFAULT_QUOTAS['quota_set']['id']
        self.assertEqual(eval(actual_value), DEFAULT_QUOTAS)
        self.delete_custom_playnetmano_rm_quota(self.resource_ids["project_id"])

    def test_get_quota_usage_for_project(self):
        self.create_instance(count=1)
        actual_usage = self.get_quota_usage_for_project(
            self.resource_ids["project_id"])
        expected_usage = self.get_usage_manually(
            self.resource_ids["project_id"])
        self.assertEqual(eval(actual_usage)["quota_set"]["ram"],
                         expected_usage["quota_set"]["ram"])
        self.assertEqual(eval(actual_usage)["quota_set"]["cores"],
                         expected_usage["quota_set"]["cores"])
        self.assertEqual(eval(actual_usage)["quota_set"]["instances"],
                         expected_usage["quota_set"]["instances"])
        self.assertEqual(eval(actual_usage)["quota_set"]["network"],
                         expected_usage["quota_set"]["network"])
        self.assertEqual(eval(actual_usage)["quota_set"]["subnet"],
                         expected_usage["quota_set"]["subnet"])
        self.assertEqual(eval(actual_usage)["quota_set"]["volumes"],
                         expected_usage["quota_set"]["volumes"])
        self.delete_instance()

    def test_playnetmano_rm_put_method_wrong_token(self):
        new_quota = {"quota_set": {"instances": 15, "cores": 10}}
        response = self.create_custom_playnetmano_rm_quota_wrong_token(
            self.resource_ids["project_id"], new_quota)
        self.assertEqual(response.status_code, 401)

    def test_playnetmano_rm_get_default_method_after_delete(self):
        new_quota = {"quota_set": {"instances": 15, "cores": 10}}
        self.create_custom_playnetmano_rm_quota(self.resource_ids["project_id"],
                                                new_quota)
        self.delete_custom_playnetmano_rm_quota(self.resource_ids["project_id"])
        actual_value = self.get_default_playnetmano_rm_quota()
        if 'id' in DEFAULT_QUOTAS['quota_set']:
            del DEFAULT_QUOTAS['quota_set']['id']
        self.assertEqual(eval(actual_value), DEFAULT_QUOTAS)
        self.delete_custom_playnetmano_rm_quota(self.resource_ids["project_id"])

    def test_quota_sync_for_project(self):
        # Delete custom quota if there are any for this project
        self.delete_custom_playnetmano_rm_quota(self.resource_ids["project_id"])
        self.create_instance()
        sync_status = self.quota_sync_for_project(
            self.resource_ids["project_id"])
        expected_status = u"triggered quota sync for " + \
            self.resource_ids["project_id"]
        calculated_limits = self.calculate_quota_limits(
            self.resource_ids["project_id"])
        self.wait_sometime_for_sync()
        actual_limits = self.get_actual_limits(self.resource_ids["project_id"])
        self.assertEqual(calculated_limits, actual_limits)
        self.assertEqual(eval(sync_status), expected_status)
        self.delete_instance()

    def test_quota_exceed_after_sync(self):
        new_quota = {"quota_set": {"instances": 2}}
        self.create_custom_playnetmano_rm_quota(self.resource_ids["project_id"],
                                                new_quota)
        self.quota_sync_for_project(self.resource_ids["project_id"])
        self.wait_sometime_for_sync()
        try:
            self.create_instance(count=3)
        except Exception as exp:
            self.assertIsInstance(exp, novaclient.exceptions.Forbidden)
            message = exp.message
        self.assertIn(u"Quota exceeded for instances", message)
        self.delete_instance()
