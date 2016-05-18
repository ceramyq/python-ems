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

import copy

import six

from lxml import etree

from ems.exceptions import SchemaException
from ems.exceptions import ValidationException

from ems.schema import fields


def parse_meta(name, bases, dct):
    """
    Parse the _META_ attribute from a schema definition.
    """
    # Set default metadata
    schema_meta = {
        # The XML tag for the root element.
        'tag': name,

        # Validate the schema values when rendering.
        'validate': True,

        # Always omit empty values for fields which are not required.
        'omit_empty': False,

        # Omit strings which are equal to ''
        'omit_blank': False,

        # Validation fails for Choice types with more than one value populated.
        'strict_choice': False,

        # Fields are validated when they're set.
        'eager_validation': False,
    }

    # Sets up defaults if the _META_ attribute is not found.
    if '_META_' in dct:
        for k, v in six.iteritems(dct['_META_']):
            schema_meta[k] = v

        # Remove original definition
        del dct['_META_']

    dct['_schema_meta'] = schema_meta


def parse_fields(name, bases, dct):
    """
    Parse the _SCHEMA_ attribute and set up the appropriate methods for each
    defined field.
    """
    if '_SCHEMA_' not in dct:
        raise SchemaException('No _SCHEMA_ attribute found for %s' % name)

    schema_fields = {}

    for k, v in six.iteritems(dct['_SCHEMA_']):
        if not isinstance(v, dict):
            raise SchemaException('Schema definitions must be dict objects')

        # Default to string type.
        field_type = v.get('type', 'string')

        # Tag name defaults to field name.
        if 'tag' not in v:
            v['tag'] = k

        # The field needs to be aware if eager validation is set.
        if 'eager_validation' not in v:
            v['eager_validation'] = dct['_schema_meta']['eager_validation']

        # Get field class from factory helper method.
        schema_fields[k] = fields.factory(field_type, **v)

        # Create new property functions for the field values.
        # Functions are wrapped to force 'k' to be evaluated now. Otherwise k
        # will always be the value of the last element in the loop.
        def wrap_get_f(k=k):
            def get_f(self):
                return self._schema_fields[k].value

            return get_f

        def wrap_set_f(k=k):
            def set_f(self, value):
                self._schema_fields[k].value = value

            return set_f

        dct[k] = property(wrap_get_f(), wrap_set_f())

    # Remove the original schema definition and add the new one
    del dct['_SCHEMA_']
    dct['_schema_fields'] = schema_fields


class WebServiceMeta(type):
    """
    Metaclass used to create new WebService objects from a schema, defined
    as a dictionary.
    """
    def __new__(meta, name, bases, dct):
        # Sets up the _schema_meta attribute.
        parse_meta(name, bases, dct)

        # Sets up the _schema_fields attribute.
        parse_fields(name, bases, dct)

        return super(WebServiceMeta, meta).__new__(meta, name, bases, dct)


class WebServiceObject(object):
    """
    Base class for objects to be serialized/deserialized for the API. Also
    used by nested objects.
    Subclasses should also use the WebServiceMeta metaclass.
    """
    def __init__(self, **kwds):
        # Ensure that the field values are NOT shared across instances of the
        # same class.
        self._schema_fields = copy.deepcopy(self._schema_fields)

        # Allow any field to be set via keyword arguments
        for k, v in six.iteritems(kwds):
            if k in self._schema_fields:
                self._schema_fields[k].value = v
            else:
                raise TypeError('%s got unexpected keyword argument %s' %
                                self.__class__.__name__, k)

    def validate(self):
        """
        Checks whether the values are valid for the class schema.
        Returns None if valid. Otherwise, raises ValidationException.
        """
        for field in six.itervalues(self._schema_fields):
            field.validate()

    def is_valid(self):
        """
        Convenience wrapper for validate() to return True or False.
        """
        try:
            self.validate()
        except ValidationException:
            return False

        return True

    def to_element(self, root_element=None):
        """
        Returns the object as an lxml.Element instance.
        """
        if root_element is None:
            root_element = etree.Element(self._schema_meta['tag'])

        for field in six.iteritems(self._schema_fields):
            if self._schema_meta['validate']:
                field.validate()

            children = field.to_element(
                omit_empty=self._schema_meta['omit_empty'],
                omit_blank=self._schema_meta['omit_blank'])

            # Append each child element if the rendered elements form a list.
            # This means that each child gets a root tag. E.g.
            # <attribute>
            #   <a>1</a>
            # </attribute>
            # <attribute>
            #   <a>2</a>
            # </attribute>
            if isinstance(children, list):
                [root_elem.append(elem)
                 for elem
                 in children]

            elif children is not None:
                root_elem.append(children)

    def render(self, pretty=False):
        """
        Renders the object into an XML string representation.
        """
        element = self.to_element()
        return etree.tostring(element, pretty_print=pretty)

    @classmethod
    def parse(cls, strict=True):
        """
        Returns a new instance of the class from an XML.
        """
        raise NotImplementedError('')
