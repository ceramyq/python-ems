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


class Field(object):
    """
    Base abstract field class.

    Subclasses must override the to_text and from_text methods to define how
    their respective values must be converted to and from XML.
    """
    def __init__(self, **kwds):
        # The default value of the field if it is not populated. There is no
        # point using `required=True` or `min_occurs=1` with this.
        self.default = None

        # The default tag is the name of the class which is probably never
        # going to be useful...
        self.tag = self.__class__.__name__

        # Fail validation if the field value is not populated.
        self.required = False

        # Do not output <tagName /> if the field is None.
        self.omit_empty = False

        # List of objs subclassing the base restriction type.
        self.restrictions = []

        # Field must occur this many times.
        self.min_occurs = 0

        # If this is > 1 or None then it's a list.
        self.max_occurs = 1

        for k, v in six.iteritems(kwds):
            self.__setattr__(k, v)

        self.value = self.default

    def __str__(self):
        return "[%(class_name)s (%(tag_name)s)]" % {
            'class_name': self.__class__.__name__,
            'tag_name': self.tag,
        }

    def __len__(self):
        if self.value is None:
            return 0
        elif self.is_list():
            return len(self.value)
        else:
            return 1

    def to_text(self, value):
        """
        Converts the given value into a text type ready to be used in XML.
        """
        if value is None:
            return None

        return six.text_type(value)

    def from_text(self, text):
        """
        Converts the text from an XML field into the proper type for this field.
        """
        if text is None:
            return None

        return six.text_type(text)

    def is_list_type(self):
        """
        Returns whether this field should be processed as a list type.
        """
        return self.max_occurs is None or self.max_occurs > 1

    def is_list(self):
        """
        Returns whether the value of this field is a list.
        """
        return isinstance(self.value, list)

    def is_none(self):
        """
        Check whether the value of this field is None.
        """
        if self.value is None:
            return True

        if self.is_list() and all([i is None for i in self.value]):
            return True

        return False

    def validate_one(self, value):
        """
        Validates a single element; used to validate each child for a list or
        values for non-list fields.
        """
        # Validate restrictions
        if self.restrictions is None or len(self.restrictions) == 0:
            return

        for restriction in self.restrictions:
            if not six.callable(restriction):
                raise SchemaException(
                    'Restriction %s for field %s is not callable' %
                    (restriction, self)
                )

            restriction(value)

        self.from_text(self.to_text(value))

    def validate(self):
        """
        Validates that a field's values are correct for the given schema of the
        field.

        Raises ValidationException if the field fails validation.
        """
        # If field is required. Populated lists require 1 non-None element.
        if self.is_none() and self.required:
            raise ValidationException("Field %s is required" % self)

        # Validate whether this should be a list, or otherwise
        if self.is_list() and not self.is_list_type():
            raise ValidationException(
                "More than one value encountered for field %s which isn't a "
                "list type" % self)

        # Validate the occurs for values in the list and validate each element
        if self.is_list():
            if self.max_occurs and len(self) > self.max_occurs:
                raise ValidationException(
                    "Too many values for field: %s" % self)

            if self.min_occurs and len(self) < self.min_occurs:
                raise ValidationException(
                    "Not enough values for field: %s" % self)

            for val in self.value:
                self.validate_one(val)

        # If it's a single value, validate it as-is
        else:
            self.validate_one(self.value)

    def is_valid(self):
        """
        Convenience wrapper for the validate method to return a boolean value.
        """
        try:
            self.validate()
        except ValidationException:
            return False

        return True

    def to_element(self, **kwds):
        """
        Returns the field object as an XML element (lxml.etree.Element).
        """
        if self.value is None and (self.omit_empty or
                                   kwds.get('omit_empty', False)):
            return None

        if self.is_list_type() and self.is_list():
            elem_list = []

            for value in self.value:
                elem = etree.Element(self.tag)

                if value is None:
                    elem.text = None
                else:
                    elem.text = self.to_text(value)

                elem_list.append(elem)

            return elem_list

        elif self.is_list_type():
            elem = etree.Element(self.tag)

            if self.value is None:
                elem.text = None
            else:
                elem.text = self.to_text(self.value)

            return [elem]

        else:
            elem = etree.Element(self.tag)

            if self.value is None:
                elem.text = None
            else:
                elem.text = self.to_text(self.value)

            return elem

    def parse(self, element):
        """
        Parse an lxml.etree element to populate the values of the field. Raises
        an XMLException if the XML is invalid for this field.
        """
        # The format of the value produced by parsing must be the result of the
        # from_text method.
        if element.text is None:
            element_value = None
        else:
            try:
                element_value = self.from_text(element.text)
            except Exception as e:
                raise XMLException(e.message)

        if self.is_list_type():
            if self.value is None:
                self.value = [element_value]

            elif isinstance(self.value, list):
                self.value.append(element_value)

            else:
                self.value = [self.value, element_value]

        else:
            self.value = element_value


class ComplexField(Field):
    """
    Represent base complex type whereby a class is required
    """
    def __init__(self, **kwds):
        try:
            self.clazz = kwds['class']
        except KeyError:
            raise SchemaException(
                '[class] attribute required for complex field %s' % self)

        del kwds['class']

        super(ComplexField, self).__init__(**kwds)

    # Replaces the from_text on Field class
    def from_single_element(self, element):
        return self.clazz.parse(element)

    # Replaces the to_text on Field class
    def to_single_element(self, value):
        root = etree.Element(self.tag)

        if value is None:
            root.text = None
        else:
            root = value.to_element(root_element=root)

        return root

    def to_element(self, **kwds):
        """ """
        if self.value is None and (self.omit_empty or
                                   kwds.get('omit_empty', False)):
            return None

        if self.is_list_type() and self.is_list():
            elem_list = []

            for value in self.value:
                elem = self.to_single_element(value)
                elem_list.append(elem)

            return elem_list

        elif self.is_list_type():
            elem = self.to_single_element(self.value)
            return [elem]

        else:
            elem = self.to_single_element(self.value)
            return elem

    def parse(self, element):
        """ """
        try:
            element_value = self.from_single_element(element)
        except Exception as e:
            raise XMLException(e.message)

        if self.is_list_type():
            if self.value is None:
                self.value = [element_value]

            elif isinstance(self.value, list):
                self.value.append(element_value)

            else:
                self.value = [self.value, element_value]

        else:
            self.value = element_value


@field_type('str', 'string')
class String(Field):
    """
    xs:string XML type
    """
    def __init__(self, **kwds):
        self.omit_blank = False
        super(String, self).__init__(**kwds)


@field_type('int', 'integer')
class Integer(Field):
    """
    xs:integer XML type
    """
    def from_text(self, text):
        return int(value)


@field_type('float')
class Float(Field):
    """
    xs:float XML type
    """
    def from_text(self, text):
        return float(text)


@field_type('bool', 'bit', 'boolean')
class Boolean(Field):
    """
    xs:boolean XML type
    """
    def to_text(self, value):
        if value is None:
            return None

        # Force bool to lowercase
        return super(Boolean, self).to_text(value).lower()

    def from_text(self, text):
        if text.lower() == 'true':
            return True
        elif text.lower() == 'false':
            return False
        else:
            return XMLException(
                '%s cannot be converted to boolean type' % text
            )


@field_type('date', 'datetime')
class Date(Field):
    """
    xs:date XML type
    """
    def to_text(self, value):
        if isinstance(value, six.string_types):
            value = self.from_text(value)

        formatter = getattr(self.value, 'isoformat', None)

        if formatter is not None and six.callable(formatter):
            return value.isoformat()

        else:
            raise ValidationException(
                'Cannot convert value %s to ISO datetime' % value)

    def from_text(self, text):
        try:
            return dateutil.parser.parse(text)
        except ValueError as e:
            raise XMLException(e.message)


@field_type('choice')
class Choice(ComplexField):
    """
    complex XML type xs:choice
    """
    def __init__(self, **kwds):
        super(Choice, self).__init__(**kwds)
        self.strict = kwds.get('strict', False)

    def validate_one(self, value):
        super(Choice, self).validate_one(value)

        if value is None:
            return

        value.validate()

        if self.strict:
            # Count the number of fields which aren't none
            populated_fields = [
                f.is_none() for f
                in six.itervalues(value._schema_fields)
            ].count(False)

            if populated_fields > 1:
                raise ValidationException(
                    'Multiple fields populated for choice field, '
                    'using strict validation')


@field_type('sequence', 'list')
class Sequence(ComplexField):
    """
    complex XML type xs:sequence
    """
    def __init__(self, **kwds):
        super(Sequence, self).__init__(**kwds)
        self.max_occurs = kwds.get('max_occurs', None)
        self.min_occurs = kwds.get('min_occurs', 0)
