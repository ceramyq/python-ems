#!/usr/bin/env python
#
# Copyright 2016 Opsview Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import six

from ems.api import ApiResourceMeta

from ems.types import customers


@six.add_metaclass(ApiResourceMeta)
class Customer(object):

    _API_SCHEMA_ = {
        'create_customer': {
            'path': 'createCustomer.xml',
            'method': 'POST',
            'returns': customers.CreateCustomerResponse,
            'params': {
                'name': {
                    'param': 'customerName',
                    'required': True,
                },
                'enabled': {
                    'param': 'isEnabled',
                    'type': 'bool',
                },
                'crm_id': {
                    'param': 'crmId',
                },
                'ref': {
                    'param': 'refId',
                },
                'identifier': {
                    'param': 'custIdentifier',
                },
                'description': {
                    'param': 'description',
                }
            },
        },
        'retrieve_customer_by_id': {
            'path': 'getCustomerById.xml',
            'method': 'GET',
            'returns': customers.CustomerDetailsResponse,
            'params': {
                'id': {
                    'param': 'customerId',
                    'required': True,
                    'type': 'int',
                }
            }
        },
        'retrieve_customer_by_name': {
            'path': 'getCustomerByName.xml',
            'method': 'GET',
            'returns': customers.CustomerDetailsResponse,
            'params': {
                'name': {
                    'param': 'customerName',
                    'required': True,
                }
            }
        },
        'update_customer': {
            'path': 'updateCustomer.xml',
            'method': 'POST',
            'returns': customers.UpdateCustomerResponse,
            'params': {
                'id': {
                    'param': 'customerId',
                    'type': 'int',
                    'required': True,
                },
                'name': {
                    'param': 'customerName',
                },
                'enabled': {
                    'param': 'isEnabled',
                    'type': 'bool',
                },
                'crm_id': {
                    'param': 'crmId',
                },
                'identifier': {
                    'param': 'custIdentifier',
                },
                'ref': {
                    'param': 'refId',
                },
                'description': {
                    'param': 'description',
                }
            }
        },
        'delete_customer': {
            'path': 'deleteCustomerById.xml',
            'method': 'POST',
            'returns': customers.DeleteCustomerResponse,
            'params': {
                'id': {
                    'param': 'customerId',
                    'type': 'int',
                    'required': True,
                },
            }
        },
        'search_customers': {
            'path': 'searchCustomers.xml',
            'method': 'GET',
            'returns': customers.SearchCustomersResponse,
            'params': {
                'name': {
                    'param': 'customerName',
                },
                'crm_id': {
                    'param': 'crmId',
                },
                'ref': {
                    'param': 'refId',
                },
                'page_index': {
                    'param': 'pageIndex',
                    'type': 'int',
                },
                'page_size': {
                    'param': 'pageSize',
                    'type': 'int,'
                },
                'sort_col': {
                    'param': 'sortCol',
                },
                'sort_order': {
                    'param': 'sortOrder',
                },
                'pattern': {
                    'param': 'searchPattern',
                }
            }
        }
    }
