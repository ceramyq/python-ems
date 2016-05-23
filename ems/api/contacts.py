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

from ems.types import contacts


@six.add_metaclass(ApiResourceMeta)
class Contact(object):

    _API_SCHEMA_ = {
        'create_contact': {
            'path': 'createContact.xml',
            'method': 'POST',
            'returns': contacts.CreateContactResponse,
            'params': {
                'locale_id': {
                    'param': 'localeId',
                    'type': 'int',
                },
                'email': {
                    'param': 'emailId',
                    'required': True,
                },
                'name': {
                    'param': 'contactName',
                },
                'number': {
                    'param': 'contactNumber',
                },
                'login_allowed': {
                    'param': 'loginAllowed',
                },
                'password': {
                    'param': 'contactPassword',
                },
                'customer_id': {
                    'param': 'customerId',
                    'type': 'int',
                },
                'shipping_address': {
                    'param': 'shipAddr',
                },
                'shipping_address_city': {
                    'param': 'shipAddrCity',
                },
                'shipping_address_country': {
                    'param': 'shipAddrCountry',
                },
                'shipping_address_state': {
                    'param': 'shipAddrState',
                },
                'shipping_address_zip': {
                    'param': 'shipAddrZip',
                },
                'billing_address': {
                    'param': 'billAddr',
                },
                'billing_address_city': {
                    'param': 'billAddrCity',
                },
                'billing_address_country': {
                    'param': 'billAddrCountry',
                },
                'billing_address_zip': {
                    'param': 'billAddrZip',
                },
                'ref1': {
                    'param': 'refId1',
                },
                'ref2': {
                    'param': 'refId2',
                },
            }
        },
        'retrieve_contact_by_id': {
            'path': 'getContactById.xml',
            'method': 'GET',
            'returns': contacts.ContactDetailsResponse,
            'params': {
                'id': {
                    'param': 'contactId',
                    'type': 'int',
                    'required': True,
                }
            }
        },
        'retrieve_contact_by_email': {
            'path': 'getContactByEmailId.xml',
            'method': 'GET',
            'returns': contacts.ContactDetailsResponse,
            'params': {
                'email': {
                    'param': 'emailId',
                    'required': True,
                }
            }
        },
        'update_contact': {
            'path': 'updateContact.xml',
            'method': 'POST',
            'returns': contacts.UpdateContactResponse,
            'params': {
                'id': {
                    'param': 'contactId',
                    'type': 'int',
                    'required': True,
                },
                'email': {
                    'param': 'emailId',
                },
                'name': {
                    'param': 'contactName',
                },
                'number': {
                    'param': 'contactNumber',
                },
                'login_allowed': {
                    'param': 'loginAllowed',
                },
                'shipping_address': {
                    'param': 'shipAddr',
                },
                'shipping_address_city': {
                    'param': 'shipAddrCity',
                },
                'shipping_address_country': {
                    'param': 'shipAddrCountry',
                },
                'shipping_address_state': {
                    'param': 'shipAddrState',
                },
                'shipping_address_zip': {
                    'param': 'shipAddrZip',
                },
                'billing_address': {
                    'param': 'billAddr',
                },
                'billing_address_city': {
                    'param': 'billAddrCity',
                },
                'billing_address_country': {
                    'param': 'billAddrCountry',
                },
                'billing_address_state': {
                    'param': 'billAddrState',
                },
                'billing_address_zip': {
                    'param': 'billAddrZip',
                },
                'ref1': {
                    'param': 'refId1',
                },
                'ref2': {
                    'param': 'refId2',
                },
                'locale_id': {
                    'param': 'localeId',
                    'type': 'int',
                },
            }
        },
        'delete_contact': {
            'path': 'deleteContact.xml',
            'method': 'GET',
            'returns': contacts.DeleteContactResponse,
            'params': {
                'id': {
                    'param': 'contactId',
                    'required': True,
                    'type': 'int',
                }
            }
        },
        'search_contacts': {
            'path': 'searchContacts.xml',
            'method': 'GET',
            'returns': contacts.SearchContactsResponse,
            'params': {
                'customer_id': {
                    'param': 'customerId',
                    'type': 'int',
                },
                'name': {
                    'param': 'customerName',
                },
                'page_index': {
                    'param': 'pageIndex',
                    'type': 'int',
                },
                'page_size': {
                    'param': 'pageSize',
                    'type': 'int',
                },
                'sort_col': {
                    'param': 'sortCol',
                },
                'sort_order': {
                    'param': 'sortOrder',
                },
                'ref1': {
                    'param': 'refId1',
                },
                'ref2': {
                    'param': 'refId2',
                },
            }
        },
        'associate_contact': {
            'path': 'associateContactWithCustomer.xml',
            'method': 'POST',
            'returns': contacts.AssociateContactResponse,
            'params': {
                'id': {
                    'param': 'contactId',
                    'type': 'int',
                },
                'customer_id': {
                    'param': 'customerId',
                    'type': 'int',
                }
            }
        },
    }
