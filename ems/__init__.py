# -*- coding: utf-8 -*-
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

"""
Global EMS API
"""

import string

import requests
import six

from unidecode import unidecode

from ems import exceptions as exc

from ems.types import contacts
from ems.types import customers
from ems.types import entitlements
from ems.types import login
from ems.types import errors


# API versioning for EMS API
DEFAULT_HEADERS = {
    'Accept': 'application/vnd.ems.v12',
}


class _ApiCall(object):
    """
    A class (acting as a method) which takes the schema for an API call to
    provide a __call__ method which will take the necessary parameters and
    return the appropriate object.
    """
    def __init__(self, session, **kwds):
        # A reference to the API session
        self.session = session

        # Parameters which may be sent to the resource
        self.params = kwds.get('params', None)

        # Class returned by call for V1 api
        self.returns = kwds.get('returns', None)

        # The resource url
        self.url = kwds['url']

        # The HTTP method used for the call
        self.method = kwds.get('method', None)

        # Class returned for errors
        self.err_returns = kwds.get('err_returns', errors.ErrorResponse)

        # A list of the parameters required for the call
        self.required_params = []

        # Saves a list of required parameters
        self.marshal_params()

    def __call__(self, **kwds):
        for param in self.required_params:
            if kwds.get(param, None) is None:
                raise exc.ValidationException(
                    'Parameter %s is required' % param
                )

        parameters = {}

        for k, v in six.iteritems(kwds):
            if k not in self.params:
                raise exc.ValidationException('Unknown parameter: %s' % k)

            if not self.is_valid(self.params[k]['type'], v):
                raise exc.ValidationException(
                    'Parameter %s must be of type %s' %
                    (k, self.params[k]['type'])
                )

            try:
                tag = self.params[k].get('param', k)
                parameters[tag] = self.as_text(v)
            except ValueError as e:
                raise exc.ValidationException(e.message)

        return self._do_request(parameters)

    def _do_request(self, parameters):
        # TODO: Add extra arguments for handling other things
        args = {
            'method': self.method,
            'url': self.url,
        }

        if self.method in ['GET', 'HEAD']:
            args['params'] = parameters
        else:
            args['data'] = parameters

        response = self.session.request(**args)

        # TODO handle response code not in ok codes
        try:
            ret = self.returns.from_text(response.text)
        except exc.XMLException as e:
            # TODO handle exception
            ret = self.err_returns.from_text(response.text)

        if isinstance(ret, self.err_returns):
            raise exc.api_exception_factory(ret)

        return ret

    def marshal_params(self):
        """
        Parses the parameters for the call.
        """
        if self.params is not None:
            for k, v in six.iteritems(self.params):
                if v.get('required', False):
                    self.required_params.append(k)

                if 'type' not in v:
                    self.params[k]['type'] = 'string'

                if 'param' not in v:
                    self.params[k]['param'] = k

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

        raise exc.ValidationException(
            'Unknown parameter type: %s' % type(value)
        )

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


class ApiSession(object):

    def __init__(self, url, username, password):
        # Session for storing cookies
        self.session = requests.session()
        self.session.headers.update(DEFAULT_HEADERS)

        # Authentication credentials
        self.username, self.password = username, password

        if url[-1] == '/':
            self.baseurl = url
        else:
            self.baseurl = url + '/'

        # Log into the API
        self.authenticate()

    def new_url(self, path):
        if path[0] == '/':
            path = path[1:]

        return self.baseurl + path

    def authenticate(self):

        if not getattr(self, '_authenticate', None):
            self._authenticate = _ApiCall(
                session=self.session,
                url=self.new_url('verifyLogin.xml'),
                method='POST',
                returns=login.LoginResponse,
                params={'userName': {'required': True},
                        'password': {'required': True}}
            )

        return self._authenticate(userName=self.username,
                                  password=self.password)

    def create_contact(self, email, locale=None, name=None, number=None,
                       login_allowed=True, password=None, customer=None,
                       ref1=None, ref2=None):

        if not getattr(self, '_create_contact', None):
            self._create_contact = _ApiCall(
                session=self.session,
                url=self.new_url('createContact.xml'),
                method='POST',
                returns=contacts.CreateContactResponse,
                params={
                    'emailId': {
                        'required': True
                    },
                    'localeId': {
                        'type': 'int',
                    },
                    'customerId': {
                        'type': 'int',
                    },
                    'loginAllowed': {
                        'type': 'bool',
                    },
                    'contactName': {},
                    'contactNumber': {},
                    'contactPassword': {},
                    'refId1': {},
                    'refId2': {},
                })

        if name:
            name = unidecode(name)

        return self._create_contact(
            emailId=email, localeId=locale, customerId=customer,
            contactName=name, contactNumber=number, loginAllowed=login_allowed,
            contactPassword=password, refId1=ref1, refId2=ref2
        )


    def update_contact(self, id, email, name=None, number=None,
                       login_allowed=True, locale=None, ref1=None, ref2=None):

        if not getattr(self, '_update_contact', None):
            self._update_contact = _ApiCall(
                session=self.session,
                url=self.new_url('updateContact.xml'),
                method='POST',
                returns=contacts.UpdateContactResponse,
                params={
                    'contactId': {
                        'type': 'int',
                        'required': True,
                    },
                    'emailId': {
                        'required': True,
                    },
                    'localeId': {
                        'type': 'int',
                    },
                    'loginAllowed': {
                        'type': 'bool',
                    },
                    'contactName': {},
                    'contactNumber': {},
                    'refId1': {},
                    'refId2': {},
                })

            if name:
                name = unidecode(name)

        return self._update_contact(
            contactId=id, emailId=email, localeId=locale, contactName=name,
            contactNumber=number, loginAllowed=login_allowed, refId1=ref1,
            refId2=ref2
        )

    def associate_contact(self, contact_id, customer_id):

        if not getattr(self, '_associate_contact', None):
            self._associate_contact = _ApiCall(
                session=self.session,
                url=self.new_url('associateContactWithCustomer.xml'),
                method='POST',
                returns=contacts.AssociateContactResponse,
                params={
                    'contactId': {
                        'type': 'int',
                        'required': True,
                    },
                    'customerId': {
                        'type': 'int',
                        'required': True,
                    }
                })

        return self._associate_contact(contactId=contact_id,
                                       customerId=customer_id)

    def search_contacts(self, email=None, customer=None, ref1=None, ref2=None):

        if not getattr(self, '_search_contacts', None):
            self._search_contacts = _ApiCall(
                session=self.session,
                url=self.new_url('searchContacts.xml'),
                method='POST',
                returns=contacts.SearchContactsResponse,
                params={
                    'customerId': {
                        'type': 'int',
                    },
                    'pageIndex': {
                        'type': 'int',
                    },
                    'pageSize': {
                        'type': 'int',
                    },
                    'emailId': {},
                    'sortCol': {},
                    'sortOrder': {},
                    'refId1': {},
                    'refId2': {},
                })

        return self._search_contacts(
            customerId=customer, emailId=email, refId1=ref1, refId2=ref2,
            pageSize=10000
        )

    def get_contact_by_email(self, email):

        if not getattr(self, '_get_contact_by_email', None):
            self._get_contact_by_email = _ApiCall(
                session=self.session,
                url=self.new_url('getContactByEmailId.xml'),
                method='GET',
                returns=contacts.ContactDetailsResponse,
                params={
                    'emailId': {
                        'required': True,
                    },
                })

        return self._get_contact_by_email(emailId=email)

    def create_customer(self, name, enabled=True, crm_id=None, ref=None):

        if not getattr(self, '_create_customer', None):
            self._create_customer = _ApiCall(
                session=self.session,
                url=self.new_url('createCustomer.xml'),
                method='POST',
                returns=customers.CreateCustomerResponse,
                params={
                    'customerName': {
                        'required': True,
                    },
                    'isEnabled': {
                        'type': 'bool',
                    },
                    'crmId': {},
                    'refId': {},
                    'custIdentifier': {},
                    'description': {}
                })

        return self._create_customer(
            customerName=name, isEnabled=enabled, crmId=crm_id, refId=ref,
            custIdentifier=None, description=None
        )

    def get_customer_by_name(self, name):

        if not getattr(self, '_get_customer_by_name', None):
            self._get_customer_by_name = _ApiCall(
                session=self.session,
                url=self.new_url('getCustomerByCustomerName.xml'),
                method='GET',
                returns=customers.CustomerDetailsResponse,
                params={'customerName': {'required': True}}
            )

        return self._get_customer_by_name(customerName=name)

    def update_customer(self, id, name=None, enabled=None, crm_id=None,
                        ref=None):

        if not getattr(self, '_update_customer', None):
            self._update_customer = _ApiCall(
                session=self.session,
                url=self.new_url('updateCustomer.xml'),
                method='POST',
                returns=customers.UpdateCustomerResponse,
                params={
                    'customerId': {
                        'type': 'int',
                        'required': True,
                    },
                    'isEnabled': {
                        'type': 'bool',
                    },
                    'custIdentifier': {},
                    'customerName': {},
                    'crmId': {},
                    'refId': {},
                    'description': {}
                })

        return self._update_customer(
            customerId=id, customerName=name, isEnabled=enabled, crmId=crm_id,
            refId=ref, custIdentifier=None, description=None
        )

    def search_customers(self, name=None, crm_id=None, ref=None):

        if not getattr(self, '_search_customers', None):
            self._search_customers = _ApiCall(
                session=self.session,
                url=self.new_url('searchCustomers.xml'),
                method='GET',
                returns=contacts.SearchCustomersResponse,
                params={
                    'pageIndex': {
                        'type': 'int',
                    },
                    'pageSize': {
                        'type': 'int,'
                    },
                    'customerName': {},
                    'crmId': {},
                    'refId': {},
                    'sortCol': {},
                    'sortOrder': {},
                    'searchPattern': {}
                })

        return self._search_customers(
            customerName=name, crmId=crm_id, refId=ref, pageSize=1000
        )

    def create_entitlement(self, customer_id, contact_id, products, start_date,
                           end_date, num_activations, cc_email=None, ref1=None,
                           ref2=None, user_registration='OPTIONAL'):

        ent = entitlements.Entitlement.create(
            customer_id=customer_id, contact_id=contact_id, products=products,
            start_date=start_date, end_date=end_date,
            num_activations=num_activations, cc_email=cc_email, ref1=ref1,
            ref2=ref2, user_registration=user_registration
        )

        response = self.session.request(
            url=self.new_url('v4_0/ws/entitlement.ws'),
            method='PUT',
            data=ent.render(),
        )

        if response.status_code != 201:
            err_code = response.headers.get('errorCode', None)
            err = response.text

            err_obj = errors.ErrorResponse(
                code=err_code,
                description=err,
                status='FAIL'
            )

            raise exc.api_exception_factory(err_obj)

        ent_id = response.headers.get('Location', None)
        ent = self.get_entitlement(ent_id)

        ent.action = 'COMMIT'
        ent.lifecycle_stage = 'COMMITTED'

        for a in ent.product_key:
            for b in a.item:
                for c in b.product:
                    for d in c.feature:
                        for e in d.license_model:
                            for f in e.attribute:
                                if f.name == 'START_DATE':
                                    f.value = start_date

                                if f.name == 'END_DATE':
                                    f.value = end_date

        return self.update_entitlement(ent)

    def get_entitlement(self, entitlement_id, is_eid=False):
        params = {}
        if is_eid:
            params['idType'] = 'Eid'
        else:
            params['idType'] = 'Entid'

        response = self.session.request(
            url=self.new_url('v4_0/ws/entitlement/%s.ws' % entitlement_id),
            method='GET',
            params=params
        )

        if response.status_code == 200:
            return entitlements.Entitlement.from_text(response.text)

        else:
            err_code = response.headers.get('errorCode', None)
            err = response.text
            err_obj = errors.ErrorResponse(
                code=err_code,
                description=err,
                status='FAIL',
            )

            raise exc.api_exception_factory(err_obj)

        return response.text

    def update_entitlement(self, entitlement):

        response = self.session.request(
            url=self.new_url('v4_0/ws/entitlement.ws'),
            method='PUT',
            data=entitlement.render(),
        )

        if response.status_code != 201:
            err_code = response.headers.get('errorCode', None)
            err = response.text

            err_obj = errors.ErrorResponse(
                code=err_code,
                description=err,
                status='FAIL'
            )

            raise exc.api_exception_factory(err_obj)

        ent_id = response.headers.get('Location', None)
        return self.get_entitlement(ent_id)
