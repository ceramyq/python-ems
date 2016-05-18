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
import datetime

import dateutil.parser
import six

from lxml import etree

from ems.exceptions import SchemaException
from ems.exceptions import ValidationException
from ems.exceptions import XMLException


field_classes = {}


def field_type(*field_names):
    """
    Decorator to register field classes for the factory.
    """
    def field_class(cls):
        for name in field_names:
            field_classes[name] = cls

        return cls

    return field_class


def factory(type_, **kwds):
    """
    Create new instance of a field.
    """
    if type_ not in field_classes:
        raise SchemaException('Unknown field type: %s' % type_)

    return field_classes[type_](**kwds)


@six.add_metaclass(abc.ABCMeta)
class Field(object):
    """
    Base abstract field class.
    """
    def __init__(self, **kwds):
        self.default = None
        self.tag = self.__class__.__name__
        self.required = False
        self.omit_empty = False
        self.restrictions = []

        for k, v in six.iteritems(kwds):
            self.__setattr__(k, v)

        self.value = self.default

    def validate(self):
        if self.value is None and self.required:
            raise ValidationException('Required field [%s (%s)] cannot be None'
                                      % self.__class__.__name__, self.tag)

        if len(self.restrictions) > 0:
            for restriction in self.restrictions:
                if not six.callable(restriction):
                    raise SchemaException(
                        'Restriction [%s] for field [%s (%s)] is not callable'
                        % restriction, self.__class__.__name__, self.tag)

                restriction(self.value)

    def is_valid(self):
        try:
            self.validate()
        except ValidationException:
            return False

        return True

    @abc.abstractmethod
    def to_element(self, **kwds):
        """
        Returns the field object as an XML element (lxml.etree.Element).
        """
        if self.omit_empty or kwds.get('omit_empty', False):
            if self.value is None:
                return None

        if getattr(self, 'omit_blank', False) or kwds.get('omit_blank', False):
            if self.value == '':
                return None

        element = etree.Element(self.tag)
        element.text = six.text_type(self.value)
        return element

    @abc.abstractmethod
    def parse(self, element):
        """
        Parse an lxml.etree element to populate the values of the field. Raises
        an XMLException if the XML is invalid for this field.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class ComplexField(Field):
    """
    Represent base complex type whereby a class is required.
    """
    def __init__(self, **kwds):
        if 'class' not in kwds:
            raise SchemaException('Class attribute expected for complex field '
                                  '[%s (%s)]' %
                                  self.__class__.__name__, self.tag)

        super(ComplexField, self).__init__(**kwds)


@field_type('str', 'string')
class String(Field):
    """
    xs:string XML type
    """
    def __init__(self, **kwds):
        self.omit_blank = False
        super(String, self).__init__(**kwds)

    def validate(self):
        super(String, self).validate()
        if self.value is not None:
            if not isinstance(self.value, six.string_types):
                raise ValidationException('String field must a string type')

    def to_element(self, **kwds):
        return super(String, self).to_element(**kwds)

    def parse(self, element):
        pass


@field_type('int', 'integer')
class Integer(Field):
    """
    xs:integer XML type
    """
    def validate(self):
        super(Integer, self).validate()
        if self.value is not None:
            if not isinstance(self.value, int):
                raise ValidationException('Integer field must be of type int')

    def to_element(self, **kwds):
        return super(Integer, self).to_element(**kwds)

    def parse(self, element):
        pass


@field_type('float')
class Float(Field):
    """
    xs:float XML type
    """
    def validate(self):
        super(Float, self).validate()
        if self.value is not None:
            if (not isinstance(self.value, float) and
                    not isinstance(self.value, int)):
                raise ValidationException('Float field must be either of type '
                                          'int or float')

    def to_element(self, **kwds):
        return super(Float, self).to_element(**kwds)

    def parse(self, element):
        pass


@field_type('bool', 'bit', 'boolean')
class Boolean(Field):
    """
    xs:boolean XML type
    """
    def validate(self):
        super(Boolean, self).validate()
        if self.value is not None:
            if not isinstance(self.value, bool):
                raise ValidationException('Boolean field must be of type bool')

    def to_element(self, **kwds):
        elem = super(Boolean, self).to_element(**kwds)
        if elem is None:
            return None

        elem.text = elem.text.lower()
        return elem

    def parse(self, element):
        pass


@field_type('date', 'datetime')
class Date(Field):
    """
    xs:date XML type
    """
    def validate(self):
        super(Date, self).validate()
        if self.value is not None:
            if isinstance(self.value, str):
                try:
                    dateutil.parser.parse(self.value)
                except ValueError:
                    raise ValidationException('Cannot parse value as ISO date')

            else:
                formatter = getattr(self.value, 'isoformat', None)
                if not six.callable(formatter):
                    raise ValidationException('No isoformat method for value')

    def to_element(self, **kwds):
        if super(Date, self).to_element(**kwds) is None:
            return None

        elem = etree.Element(self.tag)
        if isinstance(self.value, six.string_types):
            elem.text = self.value
        elif self.value is None:
            elem.text = None
        else:
            to_iso = getattr(self.value, 'isoformat', None)
            if to_iso is not None and six.callable(to_iso):
                elem.text = self.value.isoformat()
            else:
                raise ValidationException('Cannot convert value %s to ISO '
                                          'datetime' % self.value)

    def parse(self, element):
        pass


@field_type('choice')
class Choice(ComplexField):
    """
    complex XML type xs:choice
    """
    def __init__(self, **kwds):
        self.strict = False
        super(Choice, self).__init__(**kwds)

    def validate(self):
        super(Choice, self).validate()
        if self.value is not None:
            self.value.validate()

    def to_element(self, **kwds):
        if super(Choice, self).to_element(**kwds) is None:
            return None

        elem = etree.Element(self.tag)
        if self.value is None:
            elem.text = None
        else:
            self.value.to_element(root_element=elem)

        return elem

    def parse(self, element):
        pass


@field_type('sequence', 'list')
class Sequence(ComplexField):
    """
    complex XML type xs:sequence
    """
    def __init__(self, **kwds):
        self.min_occurs = 0
        self.max_occurs = None
        super(Sequence, self).__init__(**kwds)

    def validate(self):
        super(Sequence, self).validate()
        if self.value is not None:
            if isinstance(self.value, list):
                if len(self.value) < self.min_occurs:
                    raise ValidationException('Field must have at least %d '
                                              'elements in sequence' %
                                              self.min_occurs)

                if len(self.value) > self.max_occurs:
                    raise ValidationException('Field exceeds the maximum number'
                                              ' of elements for the sequence')

                [child.validate()
                 for child
                 in self.value]
            else:
                self.value.validate()

    def to_element(self, **kwds):
        if super(Sequence, self).to_element(**kwds) is None:
            return None

        elements = []

        if isinstance(self.value, list):
            for child in self.value:
                elem = etree.Element(self.tag)
                child.to_element(root_element=elem)
                elements.append(elem)

        elif self.value is None:
            elem = etree.Element(self.tag)
            elem.text = None
            elements.append(elem)

        else:
            elem = etree.Element(self.tag)
            self.value.to_element(root_element=elem)
            elements.append(elem)

        return elements

    def parse(self, element):
        pass
