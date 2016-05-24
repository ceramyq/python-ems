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


class EMSException(Exception):
    """
    Base exception.
    """
    pass


class SchemaException(EMSException):
    """
    Exceptions pertaining to schema definitions.
    """
    pass


class ValidationException(EMSException):
    """
    Exceptions pertaining to validation of values as per their given schemas.
    """
    pass


class RestrictionException(ValidationException):
    """
    Exceptions pertaining to user-defined restrictons for field values.
    """
    pass


class XMLException(EMSException):
    """
    Exceptions pertaining to parsing of XML into objects.
    """
    pass


class EMSAPIException(EMSException):
    """
    Exceptions pertaining to the Sentinel EMS API.
    """
    def __init__(self, ems_error):
        self.code = ems_error.code
        self.description = ems_error.description

        message = "[%d] %s" % (ems_error.code, ems_error.description)
        super(EMSException, self).__init__(ems_error.message)


api_exceptions = {}


def register_api_exception(cls):
    api_exceptions[cls.error_code] = cls
    return cls


def api_exception_factory(err):
    """
    Generates the correct EMS exception based on the exception code.
    """
    if err.code in api_exceptions:
        raise api_exceptions[err.code](err)
    else:
        raise EMSAPIException(err)


@register_api_exception
class InvalidParameterException(EMSAPIException):
    error_code = 100


@register_api_exception
class UnauthorizedException(EMSAPIException):
    error_code = 101


@register_api_exception
class InvalidDataException(EMSAPIException):
    error_code = 102


@register_api_exception
class InternalErrorException(EMSAPIException):
    error_code = 107


@register_api_exception
class InternalErrorException(EMSAPIException):
    error_code = 107


@register_api_exception
class InvalidSortOrderException(InvalidParameterException):
    error_code = 109


@register_api_exception
class InvalidPageIndexException(InvalidParameterException):
    error_code = 110


@register_api_exception
class InvalidPageSizeException(InvalidParameterException):
    error_code = 111


@register_api_exception
class InvalidBooleanException(InvalidParameterException):
    error_code = 113


@register_api_exception
class ValueTooLongException(InvalidParameterException):
    error_code = 115


@register_api_exception
class InvalidRegularExpressionException(EMSAPIException):
    error_code = 117


@register_api_exception
class InvalidIntegerException(InvalidParameterException):
    error_code = 118


@register_api_exception
class MinimumValueException(InvalidParameterException):
    error_code = 120


@register_api_exception
class RequiredFieldException(InvalidParameterException):
    error_code = 122


@register_api_exception
class InvalidSortColumnException(InvalidParameterException):
    error_code = 124


@register_api_exception
class RequestedResourceNotFoundException(InvalidParameterException):
    error_code = 125


@register_api_exception
class SystemException(InvalidParameterException):
    error_code = 127


@register_api_exception
class LoginRequiredException(InvalidParameterException):
    error_code = 128


@register_api_exception
class NoSuchCustomerException(InvalidParameterException):
    error_code = 512


@register_api_exception
class NoSuchContactException(InvalidParameterException):
    error_code = 513


@register_api_exception
class CustomerAlreadyAssocatedException(InvalidParameterException):
    error_code = 514


@register_api_exception
class CannotModifyContactInfoException(InvalidParameterException):
    error_code = 516


@register_api_exception
class ContactNotFoundWithIDException(InvalidParameterException):
    error_code = 518


@register_api_exception
class InvalidCustomerIDException(InvalidParameterException):
    error_code = 519


@register_api_exception
class CustomerAlreadyExistsException(InvalidParameterException):
    error_code = 521


@register_api_exception
class ContactNotUniqueException(InvalidParameterException):
    error_code = 522


@register_api_exception
class NoEmailAddressException(InvalidParameterException):
    error_code = 523


@register_api_exception
class NewBlankPasswordException(InvalidParameterException):
    error_code = 524


@register_api_exception
class OldBlankPasswordException(InvalidParameterException):
    error_code = 525


@register_api_exception
class IncorrectUsernameOrPasswordException(InvalidParameterException):
    error_code = 526


@register_api_exception
class InvalidEmailException(InvalidParameterException):
    error_code = 528


@register_api_exception
class DuplicateEmailAddressException(InvalidParameterException):
    error_code = 529


@register_api_exception
class UserRegistrationDisallowedException(InvalidParameterException):
    error_code = 532


@register_api_exception
class PasswordTooShortException(InvalidParameterException):
    error_code = 533


@register_api_exception
class EntitlementExistsForContactException(EMSAPIException):
    error_code = 611


@register_api_exception
class EntitlementExistsForCustomerException(EMSAPIException):
    error_code = 694


@register_api_exception
class InvalidNumericValueException(InvalidParameterException):
    error_code = 714


@register_api_exception
class InvalidDateException(InvalidParameterException):
    error_code = 715


@register_api_exception
class DuplicateCustomerException(EMSAPIException):
    error_code = 902
