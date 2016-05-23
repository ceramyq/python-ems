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


from ems.schema import base
from ems.schema import fields


@base.webservice_meta(tag='user', omit_empty=True)
class User(base.WebServiceObject):
    """
    The User model used by the v4_0/ws/user.ws endpoint.
    """

    @base.webservice_meta(omit_empty=True)
    class RoleIdentifier(base.WebServiceObject):

        _SCHEMA_ = {
            'id': {
                'tag': 'roleId',
                'type': 'int',
            },
            'name': {
                'tag': 'roleName',
            },
        }

    _SCHEMA_ = {
        'username': {
            'tag': 'userName',
            'required': True,
        },
        'ref1': {
            'tag': 'refId1',
        },
        'ref2': {
            'tag': 'refId2',
        },
        'email': {
            'tag': 'emailId',
            'required': True
        },
        'locked': {
            'tag': 'isLocked',
            'type': 'bool',
        },
        'expired': {
            'tag': 'expiresOn',
            'type': 'date',
        },
        'role': {
            'tag': 'roleIdentifier',
            'type': 'choice',
            'class': RoleIdentifier,
        }
    }


@base.webservice_meta(tag='EMSResponse', omit_empty=True)
class UserListResponse(base.WebServiceObject):

    @base.webservice_meta(omit_empty=True)
    class User(base.WebServiceObject):
        _SCHEMA_ = {
            'user': {
                'tag': 'user',
                'type': 'string',
                'max_occurs': None,
            }
        }

    _SCHEMA_ = {
        'status': {
            'tag': 'stat',
            'required': True,
        },
        'users': {
            'tag': 'users',
            'type': 'sequence',
            'max_occurs': 1,
            'min_occurs': 1,
            'class': User,
        }
    }


if __name__ == "__main__":
    u = UserListResponse.from_file('/tmp/userlist.xml')
    u.validate()

    print(u.render(pretty=True))
