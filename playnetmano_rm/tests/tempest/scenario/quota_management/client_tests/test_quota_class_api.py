from playnetmano_rm.tests.tempest.scenario.quota_management. \
    client_tests import base

DEFAULT_CLASS = "default"


class Playnetmano_rmQuotaClassTestJSON(base.BasePlaynetmano_rmTest):

    def test_plrm_quota_class_put_method(self):
        new_quota = {"quota_class_set": {"instances": 15, "cores": 10}}
        actual_value = self.update_quota_for_class(self.class_name,
                                                   new_quota)
        new_quota["quota_class_set"].update({"id": self.class_name})
        self.assertEqual(new_quota, eval(actual_value))
        self.delete_quota_for_class(self.class_name)

    def test_plrm_quota_class_get_method(self):
        new_quota = {"quota_class_set": {"instances": 15, "cores": 10}}
        self.update_quota_for_class(self.class_name,
                                    new_quota)
        actual_value = self.get_quota_for_class(self.class_name)
        new_quota["quota_class_set"].update({'id': self.class_name})
        self.assertEqual(new_quota, eval(actual_value))
        self.delete_quota_for_class(self.class_name)

    def test_plrm_quota_class_delete_method(self):
        new_quota = {"quota_class_set": {"instances": 15, "cores": 10}}
        self.update_quota_for_class(self.class_name,
                                    new_quota)
        self.delete_quota_for_class(self.class_name)
        quota_after_delete = eval(self.get_quota_for_class(
            self.class_name))
        self.assertNotIn("cores", quota_after_delete["quota_class_set"])
        self.assertNotIn("instances", quota_after_delete["quota_class_set"])

    def test_plrm_quota_class_wrong_input(self):
        new_quota = {"quota_class_unset": {"instances": 15, "cores": 10}}
        actual_value = self.update_quota_for_class(self.class_name,
                                                   new_quota)
        self.assertIn("Missing quota_class_set in the body", actual_value)

    def test_plrm_quota_class_wrong_quotas(self):
        new_quota = {"quota_class_set": {"instan": 15, "cor": 10}}
        actual_value = self.update_quota_for_class(self.class_name,
                                                   new_quota)
        self.assertEmpty(actual_value)

    def test_plrm_quota_default_class_get_method(self):
        actual_value = self.get_quota_for_class(DEFAULT_CLASS)
        expected_value = {"quota_class_set": base.DEFAULT_QUOTAS["quota_set"]}
        expected_value["quota_class_set"].update({"id": DEFAULT_CLASS})
        self.assertEqual(eval(actual_value), expected_value)

    def test_plrm_quota_class_get_method_wrong_class_name(self):
        actual_value = self.get_quota_for_class("no_class")
        expected_value = {"quota_class_set": {"id": "no_class"}}
        self.assertEqual(eval(actual_value), expected_value)
