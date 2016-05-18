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


import abc

import six

from ems.exceptions import RestrictionException
from ems.exceptions import SchemaException


@six.add_metaclass(abc.ABCMeta)
class FieldRestriction(object):

    @abc.abstractmethod
    def __call__(self, value):
        pass


class EnumRestriction(FieldRestriction):
    """
    Restriction to limit the possible values applied to a field.
    """
    def __init__(self, *allowed_values):
        if allowed_values is None or len(allowed_values) < 1:
            raise SchemaException('Enumeration restriction must have at least '
                                  '1 allowed value')

        self.allowed_values = allowed_values

    def __call__(self, value):
        if value not in self.allowed_values and value is not None:
            raise RestrictionException('Value %s is not allowed for field' %
                                       element_value)
