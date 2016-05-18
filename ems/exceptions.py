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
    pass
