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


from ems import types
from ems.schema import base
from ems.schema import fields


UpdateCustomerResponse = types.StatusResponse

DeleteCustomerResponse = types.StatusResponse


@base.webservice_meta(tag='EMSResponse', omit_empty=True)
class CreateCustomerResponse(base.WebServiceObject):

    _SCHEMA_ = {
        'id': {
            'tag': 'customerId',
            'type': 'int',
        },
        'status': {
            'tag': 'stat',
        }
    }


@base.webservice_meta(tag='EMSResponse', omit_empty=True)
class CustomerDetailsResponse(base.WebServiceObject):

    @base.webservice_meta(omit_empty=True)
    class ContactList(base.WebServiceObject):

        @base.webservice_meta(omit_empty=True)
        class Contact(base.WebServiceObject):

            _SCHEMA_ = {
                'admin': {
                    'tag': 'admin',
                    'type': 'bool',
                },
                'email': {
                    'tag': 'contactEmail',
                },
                'id': {
                    'tag': 'contactId',
                    'type': 'int',
                },
                'name': {
                    'tag': 'contactName',
                },
                'number': {
                    'tag': 'contactNumber',
                },
                'customer_name': {
                    'tag': 'customerName',
                },
                'identifier': {
                    'tag': 'custIdentifier',
                },
                'status': {
                    'tag': 'status',
                    'type': 'bool',
                },
            }

        _SCHEMA_ = {
            'contact': {
                'tag': 'contact',
                'type': 'sequence',
                'max_occurs': None,
                'class': Contact,
            }
        }

    _SCHEMA_ = {
        'id': {
            'tag': 'customerId',
            'type': 'int',
        },
        'name': {
            'tag': 'customerName',
        },
        'identifier': {
            'tag': 'custIdentifier',
        },
        'description': {
            'tag': 'desc'
        },
        'enabled': {
            'tag': 'enabled',
            'type': 'bool',
        },
        'ref': {
            'tag': 'refId',
        },
        'contacts': {
            'tag': 'contacts',
            'type': 'sequence',
            'max_occurs': 1,
            'class': ContactList,
        },
        'crm_id': {
            'tag': 'cstmrcrmid',
        },
        'status': {
            'tag': 'stat',
        },
    }


@base.webservice_meta(tag='EMSresponse', omit_empty=True)
class SearchCustomersResponse(base.WebServiceObject):

    @base.webservice_meta(omit_empty=True)
    class CustomerList(base.WebServiceObject):

        @base.webservice_meta(omit_empty=True)
        class Customer(base.WebServiceObject):

            _SCHEMA_ = {
                'crm_id': {
                    'tag': 'cstmrcrmid',
                },
                'id': {
                    'tag': 'cstmrid',
                    'type': 'int',
                },
                'name': {
                    'tag': 'cstmrname',
                },
                'identifier': {
                    'tag': 'customerIdentifier',
                },
                'description': {
                    'tag': 'desc',
                },
                'enabled': {
                    'tag': 'enabled',
                    'type': 'bool',
                },
                'ref': {
                    'tag': 'refId'
                }
            }

        _SCHEMA_ = {
            'customer': {
                'tag': 'customer',
                'max_occurs': None,
                'type': 'sequence',
                'class': Customer,
            }
        }

    _SCHEMA_ = {
        'customers': {
            'tag': 'customers',
            'type': 'sequence',
            'max_occurs': 1,
            'class': CustomerList,
        },
        'status': {
            'tag': 'stat',
        },
        'total': {
            'tag': 'total',
            'type': 'int',
        }
    }
