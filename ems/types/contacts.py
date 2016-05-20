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


UpdateContactResponse = types.StatusResponse

DeleteContactResposne = types.StatusResponse

AssociateContactResponse = types.StatusResponse


@base.webservice_meta(tag='EMSResponse', omit_empty=True)
class CreateContactResponse(base.WebServiceObject):

    _SCHEMA_ = {
        'id': {
            'tag': 'contactId',
            'type': 'int',
        },
        'status': {
            'tag': 'stat',
        },
    }


@base.webservice_meta(tag='EMSResponse', omit_empty=True)
class ContactDetailsResponse(base.WebServiceObject):

    @base.webservice_meta(omit_empty=True)
    class Customer(base.WebServiceObject):

        _SCHEMA_ = {
            'id': {
                'tag': 'customerId',
                'type': 'int',
            },
            'name': {
                'tag': 'customerName',
            },
        }

    _SCHEMA_ = {
        'billing_address': {
            'tag': 'billAddr',
        },
        'billing_address_city': {
            'tag': 'billAddrCity',
        },
        'billing_address_country': {
            'tag': 'billAddrCountry',
        },
        'billing_address_state': {
            'tag': 'billAddrState',
        },
        'billing_address_zip': {
            'tag': 'billAddrZip',
        },
        'email': {
            'tag': 'contactEmail',
        },
        'id': {
            'tag': 'contactId',
        },
        'name': {
            'tag': 'contactName',
        },
        'number': {
            'tag': 'contactNumber'
        },
        'create_datetime': {
            'tag': 'createDateTime',
        },
        'customer': {
            'tag': 'customer',
            'type': 'sequence',
            'max_occurs': 1,
            'class': Customer,
        },
        'locale': {
            'tag': 'locale',
        },
        'login_allowed': {
            'tag': 'loginAllowed',
            'type': 'bool',
        },
        'ref1': {
            'tag': 'refId1',
        },
        'ref2': {
            'tag': 'refId2',
        },
        'shipping_address': {
            'tag': 'shipAddr',
        },
        'shipping_address_city': {
            'tag': 'shipAddrCity',
        },
        'shipping_address_country': {
            'tag': 'shipAddrCountry',
        },
        'shipping_address_state': {
            'tag': 'shipAddrState',
        },
        'shipping_address_zip': {
            'tag': 'shipAddrZip',
        },
        'status': {
            'tag': 'stat',
        },
        'user_registered': {
            'tag': 'userRegistered',
            'type': 'bool',
        },
    }


@base.webservice_meta(tag='EMSResponse', omit_empty=True)
class ChangeContactPasswordResponse(base.WebServiceObject):

    _SCHEMA_ = {
        'message': {
            'tag': 'message',
        },
        'status': {
            'tag': 'stat',
        }
    }


@base.webservice_meta(tag='EMSResponse', omit_empty=True)
class SearchContactsResponse(base.WebServiceObject):

    @base.webservice_meta(omit_empty=True)
    class ContactList(base.WebServiceObject):

        @base.webservice_meta(omit_empty=True)
        class Contact(base.WebServiceObject):

            _SCHEMA_ = {
                'admin': {
                    'tag': 'admin',
                    'type': 'bool',
                },
                'number': {
                    'tag': 'contNumber',
                },
                'id': {
                    'tag': 'contactId',
                    'type': 'int',
                },
                'name': {
                    'tag': 'contactName',
                },
                'email': {
                    'tag': 'emailId',
                },
                'entitlement_count': {
                    'tag': 'entitlementCount',
                    'type': 'int',
                },
                'ref1': {
                    'tag': 'refId1',
                },
                'ref2': {
                    'tag': 'refId2',
                },
                'status': {
                    'tag': 'status',
                    'type': 'bool',
                },
                'user_registered': {
                    'tag': 'userRegistered',
                    'type': 'bool',
                }
            }

        _SCHEMA_ = {
            'contact': {
                'tag': 'contact',
                'type': 'sequence',
                'class': Contact,
            }
        }

    _SCHEMA_ = {
        'contacts': {
            'tag': 'contacts',
            'type': 'sequence',
            'max_occurs': 1,
            'class': ContactList,
        },
        'status': {
            'tag': 'stat',
        },
        'total': {
            'tag': 'total',
            'type': 'int',
        },
    }
