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


import requests
import six

from ems.types import contacts
from ems.types import customers
from ems.types import errors

from ems.exceptions import EMSAPIException
from ems.exceptions import ValidationException
from ems.exceptions import XMLException


# Headers to always be added to API requests to Safenet EMS
DEFAULT_HEADERS = {
    'Accept': 'application/vnd.ems.v12',
}


API_BROKER = None


def get_instance(*args, **kwds):
    return ApiBroker.get_instance(*args, **kwds)


class ApiBroker(object):

    def __init__(self, url, username, password):

        # Number of consecutive failed logins.
        self.failed_logins = 0

        # Number of failed logins before giving up.
        self.max_failed_logins = 3

        # Set up the base URL of the EMS instance
        if url[-1] == '/':
            self.base_url = url
        else:
            self.base_url = url + '/'

        # Store cookes et. al
        self.session = requests.session()

        # Use default headers at a minumum
        self.add_headers(DEFAULT_HEADERS)

        # Store authentication credentials for EMS
        self.username, self.password = username, password

        # Log into the API
        self.authenticate()

    def add_headers(self, headers):
        """
        Add headers to those used by the session.
        """
        self.session.headers.update(headers)

    @classmethod
    def get_instance(cls, *args, **kwds):
        """
        Returns a single instance of the API broker to prevent creating multiple
        entities.
        """
        global API_BROKER

        if not API_BROKER:
            API_BROKER = cls(*args, **kwds)

        return API_BROKER

    def build_url(self, path):
        """
        Return a new URL using the path, based on the original URL.
        """
        return self.base_url + path

    def authenticate(self):
        return self.request(method='POST',
                            path='verifyLogin.xml',
                            data={'userName': self.username,
                                  'password': self.password})

    def request(self, method, path, data=None):
        if method in ['GET', 'HEAD']:
            return self._request(method=method,
                                 url=self.build_url(path),
                                 params=data)

        return self._request(method=method,
                             url=self.build_url(path),
                             data=data)

    def _request(self, *args, **kwds):
        return self.session.request(*args, **kwds)


class ApiCall(object):

    def __init__(self, **kwds):
        # Parameters which may be sent to the resource
        self.params = kwds.get('params', None)

        # The path to the resource, after the /ems/ path
        self.path = kwds.get('path', None)

        # The HTTP method used for the call
        self.method = kwds.get('method', None)

        # The class returned by the call
        self.returns = kwds.get('returns', None)

        # Class returned for errors
        self.err_returns = kwds.get('err_returns', errors.ErrorResponse)

        # A list of the parameters required for the call
        self.required_params = []

        # Saves a list of required parameters
        self.marshal_params()

        # Store the API broker instance once it's been called
        self.api_broker = None

        # Status codes which indicate that it was successful
        self.ok_codes = kwds.get('ok_codes', [200, 201])

    def __call__(self, **kwds):
        for param in self.required_params:
            if kwds.get(param, None) is None:
                raise ValidationException('Parameter %s is required' % param)

        parameters = {}

        for k, v in six.iteritems(kwds):
            if k not in self.params:
                raise ValidationException('Unknown parameter: %s' % k)

            if not self.is_valid(self.params[k]['type'], v):
                raise ValidationException('Parameter %s must be of type %s' %
                                          (k, self.params[k]['type']))

            try:
                tag = self.params[k]['param']
                parameters[tag] = self.as_text(v)
            except ValueError as e:
                raise ValidationException(e.message)

        return self._do_request(parameters)

    @staticmethod
    def as_text(value):
        if value is None:
            return None

        if isinstance(value, int):
            return six.text_type(value)

        if isinstance(value, six.string_types):
            return six.text_type(value)

        if isinstance(value, bool):
            return six.text_type(value).lower()

        raise ValidationException('Unknown parameter type: %s' % type(value))

    @staticmethod
    def is_valid(type_, value):
        if value is None:
            return True

        if type_ == 'bool':
            return isinstance(value, bool)

        if type_ == 'string':
            return isinstance(value, six.string_types)

        if type_ == 'int':
            return isinstance(value, int)

        return False

    def _do_request(self, parameters):
        if self.api_broker is None:
            self.api_broker = ApiBroker.get_instance()

        response = self.api_broker.request(
            method=self.method,
            path=self.path,
            data=parameters,
        )

        # TODO handle response code not in ok codes
        try:
            ret = self.returns.from_text(response.text)
        except XMLException as e:
            # TODO handle exception
            try:
                ret = self.err_returns.from_text(response.text)
            except Exception:
                raise e

        if isinstance(ret, self.err_returns):
            raise EMSAPIException(ret)

        return ret

    def marshal_params(self):
        if self.params is not None:
            for k, v in six.iteritems(self.params):
                if v.get('required', False):
                    self.required_params.append(k)

                if 'type' not in v:
                    self.params[k]['type'] = 'string'

                if 'param' not in v:
                    self.params[k]['param'] = k


class ApiResourceMeta(type):

    def __new__(meta, name, bases, dct):
        if '_API_SCHEMA_' in dct:
            for key, val in six.iteritems(dct['_API_SCHEMA_']):
                dct[key] = ApiCall(**val)

        del dct['_API_SCHEMA_']

        return super(ApiResourceMeta, meta).__new__(meta, name, bases, dct)


@six.add_metaclass(ApiResourceMeta)
class Contacts(object):

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
                'email': {
                    'param': 'emailId',
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


@six.add_metaclass(ApiResourceMeta)
class Customers(object):

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
