
from pecan import request

import playnetmano_rm.common.context as k_context


def extract_context_from_environ():
    context_paras = {'auth_token': 'HTTP_X_AUTH_TOKEN',
                     'user': 'HTTP_X_USER_ID',
                     'project': 'HTTP_X_TENANT_ID',
                     'user_name': 'HTTP_X_USER_NAME',
                     'tenant_name': 'HTTP_X_PROJECT_NAME',
                     'domain': 'HTTP_X_DOMAIN_ID',
                     'user_domain': 'HTTP_X_USER_DOMAIN_ID',
                     'project_domain': 'HTTP_X_PROJECT_DOMAIN_ID',
                     'request_id': 'openstack.request_id'}

    environ = request.environ

    for key in context_paras:
        context_paras[key] = environ.get(context_paras[key])
    role = environ.get('HTTP_X_ROLE')

    context_paras['is_admin'] = role == 'admin'
    return k_context.RequestContext(**context_paras)
