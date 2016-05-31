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

from ems.schema import base
from ems.schema import restrictions


@base.webservice_meta(tag='entitlement', omit_empty=True)
class Entitlement(base.WebServiceObject):

    @base.webservice_meta(omit_empty=True)
    class CustomerIdentifier(base.WebServiceObject):
        _SCHEMA_ = {
            'id': {
                'tag': 'customerId',
                'type': 'int'
            },
            'name': {
                'tag': 'customerName'
            },
            'identifier': {
                'tag': 'custIdentifier'
            }
        }

    @base.webservice_meta(omit_empty=True)
    class ContactIdentifier(base.WebServiceObject):
        _SCHEMA_ = {
            'id': {
                'tag': 'contactId',
                'type': 'int',
            },
            'email': {
                'tag': 'emailId',
            }
        }

    @base.webservice_meta(omit_empty=True)
    class ChannelPartnerIdentifier(base.WebServiceObject):
        _SCHEMA_ = {
            'id': {
                'tag': 'channelPartnerId',
                'type': 'int',
            },
            'name': {
                'tag': 'channelPartnerName',
            }
        }

    @base.webservice_meta(omit_empty=True)
    class CustomAttribute(base.WebServiceObject):
        _SCHEMA_ = {
            'name': {
                'tag': 'attributeName',
                'required': True,
            },
            'value': {
                'tag': 'attributeValue',
            }
        }

    @base.webservice_meta(omit_empty=True)
    class TxnHistory(base.WebServiceObject):
        _SCHEMA_ = {
            'eid': {
                'tag': 'eid',
            },
            'ent_id': {
                'tag': 'entId',
            },
            'operation': {
                'tag': 'operation',
            },
            'date': {
                'tag': 'operationDate',
                'type': 'date',
            },
            'by': {
                'tag': 'operationBy'
            },
        }

    @base.webservice_meta(omit_empty=True)
    class ProductKey(base.WebServiceObject):

        @base.webservice_meta(omit_empty=True)
        class ProductKeyItem(base.WebServiceObject):

            @base.webservice_meta(omit_empty=True)
            class EnforcementIdentifier(base.WebServiceObject):
                # EnforcementIdentifier
                _SCHEMA_ = {
                    'name': {
                        'tag': 'enforcementName',
                    },
                    'version': {
                        'tag': 'enforcementVersion',
                        'type': 'string',
                    }
                }

            @base.webservice_meta(omit_empty=True)
            class SuiteIdentifier(base.WebServiceObject):

                @base.webservice_meta(omit_empty=True)
                class SuiteNameVersion(base.WebServiceObject):
                    # SuiteNameVersion
                    _SCHEMA_ = {
                        'name': {
                            'tag': 'suiteName',
                            'required': True,
                        },
                        'version': {
                            'tag': 'suiteVersion',
                        },
                    }

                # SuiteIdentifier
                _SCHEMA_ = {
                    'id': {
                        'tag': 'suiteId',
                    },
                    'name_version': {
                        'tag': 'suiteNameVersion',
                        'type': 'sequence',
                        'class': SuiteNameVersion,
                    }
                }

            @base.webservice_meta(omit_empty=True)
            class Product(base.WebServiceObject):

                @base.webservice_meta(omit_empty=True)
                class ProductIdentifier(base.WebServiceObject):

                    @base.webservice_meta(omit_empty=True)
                    class ProductNameVersion(base.WebServiceObject):
                        # ProductNameVersion
                        _SCHEMA_ = {
                            'name': {
                                'tag': 'productName',
                            },
                            'version': {
                                'tag': 'productVersion',
                            }
                        }

                    # ProductIdentifier
                    _SCHEMA_ = {
                        'id': {
                            'tag': 'productId',
                            'type': 'int',
                        },
                        'external_id': {
                            'tag': 'prdExternalId',
                            'type': 'int',
                        },
                        'name_version': {
                            'tag': 'productNameVersion',
                            'type': 'sequence',
                            'class': ProductNameVersion,
                        }
                    }

                @base.webservice_meta(omit_empty=True)
                class Feature(base.WebServiceObject):

                    @base.webservice_meta(omit_empty=True)
                    class FeatureIdentifier(base.WebServiceObject):

                        @base.webservice_meta(omit_empty=True)
                        class FeatureNameVersion(base.WebServiceObject):
                            # FeatureNameVersion
                            _SCHEMA_ = {
                                'name': {
                                    'tag': 'featureName',
                                    'required': True,
                                },
                                'version': {
                                    'tag': 'featureVersion',
                                }
                            }

                        # FeatureIdentifier
                        _SCHEMA_ = {
                            'id': {
                                'tag': 'featureId',
                                'type': 'int',
                            },
                            'external_id': {
                                'tag': 'ftrExternalId',
                            },
                            'identity': {
                                'tag': 'featureIdentity',
                                'type': 'string',
                            },
                            'name_version': {
                                'tag': 'ftrNameVersion',
                                'type': 'sequence',
                                'class': FeatureNameVersion,
                            }
                        }

                    @base.webservice_meta(omit_empty=True)
                    class LicenseModel(base.WebServiceObject):

                        @base.webservice_meta(omit_empty=True)
                        class LicenseModelIdentifier(base.WebServiceObject):
                            # LicenseModelIdentifier
                            _SCHEMA_ = {
                                'id': {
                                    'tag': 'licenseModelId',
                                    'type': 'int',
                                },
                                'name': {
                                    'tag': 'licenseModelName',
                                }
                            }

                        @base.webservice_meta(omit_empty=True)
                        class LicenseModelAttribute(base.WebServiceObject):
                            # LicenseModelAttribute
                            _SCHEMA_ = {
                                'name': {
                                    'tag': 'Name',
                                    'required': True,
                                },
                                'value': {
                                    'tag': 'value',
                                }
                            }

                        # LicenseModel
                        _SCHEMA_ = {
                            'identifier': {
                                'tag': 'licenseModelIdentifier',
                                'type': 'choice',
                                'class': LicenseModelIdentifier,
                                'required': True,
                            },
                            'attribute': {
                                'type': 'sequence',
                                'tag': 'attribute',
                                'class': LicenseModelAttribute,
                            }
                        }

                    # Feature
                    _SCHEMA_ = {
                        'identifier': {
                            'tag': 'featureIdentifier',
                            'type': 'choice',
                            'class': FeatureIdentifier,
                        },
                        'license_model': {
                            'tag': 'licenseModel',
                            'type': 'sequence',
                            'class': LicenseModel,
                        },
                        'item_feature_state': {
                            'tag': 'itemFeatureState',
                            # TODO(JG): should have enum restriction but
                            # field is not in XSD
                        }
                    }

                # Product
                _SCHEMA_ = {
                    'identifier': {
                        'tag': 'productIdentifier',
                        'type': 'choice',
                        'class': ProductIdentifier,
                    },
                    'feature': {
                        'tag': 'feature',
                        'type': 'sequence',
                        'class': Feature,
                    },
                }

            @base.webservice_meta(omit_empty=True)
            class CommonLicenseAttributes(base.WebServiceObject):

                @base.webservice_meta(omit_empty=True)
                class Attribute(base.WebServiceObject):
                    # Attribute
                    _SCHEMA_ = {
                        'name': {
                            'tag': 'Name',
                            'required': True,
                        },
                        'value': {
                            'tag': 'value',
                        }
                    }

                # CommonLicenseAttributes
                _SCHEMA_ = {
                    'attribute': {
                        'tag': 'attribute',
                        'type': 'sequence',
                        'class': Attribute,
                    }
                }

            @base.webservice_meta(omit_empty=True)
            class ActivationAttributes(base.WebServiceObject):

                @base.webservice_meta(omit_empty=True)
                class AttributeGroup(base.WebServiceObject):

                    @base.webservice_meta(omit_empty=True)
                    class Attribute(base.WebServiceObject):
                        # Attribute
                        _SCHEMA_ = {
                            'name': {
                                'tag': 'attributeName',
                            },
                            'value': {
                                'tag': 'attributeValue',
                            },
                            'read_only': {
                                'tag': 'readOnly',
                                'type': 'bool',
                            },
                            'mandatory': {
                                'tag': 'mandatory',
                                'type': 'bool',
                            },
                        }

                    # AttributeGroup
                    _SCHEMA_ = {
                        'attribute': {
                            'type': 'sequence',
                            'tag': 'attribute',
                            'class': Attribute,
                        }
                    }

                # ActivationAttributes
                _SCHEMA_ = {
                    'group': {
                        'type': 'sequence',
                        'tag': 'attributeGroup',
                        'class': AttributeGroup,
                    },
                }

            @base.webservice_meta(omit_empty=True)
            class EntitlementExtension(base.WebServiceObject):
                # EntitlementExtension
                _SCHEMA_ = {
                }

            @base.webservice_meta(omit_empty=True)
            class CustomAttribute(base.WebServiceObject):
                # CustomAttribute
                _SCHEMA_ = {
                }

            # ProductKeyItem
            _SCHEMA_ = {
                'enforcement_identifier': {
                    'tag': 'enforcementIdentifier',
                    'type': 'sequence',
                    'class': EnforcementIdentifier,
                },
                'id': {
                    'tag': 'ItemId',
                    'type': 'int',
                },
                'total_quantity': {
                    'tag': 'totalQuantity',
                    'type': 'int',
                    'default': 1,
                },
                'available_quantity': {
                    'tag': 'availableQuantity',
                    'type': 'int',
                },
                'item_state': {
                    'tag': 'itemState',
                    'type': 'int',
                },
                'activation_method': {
                    'tag': 'activationMethod',
                    'restrictions': [
                        restrictions.EnumRestriction('FIXED',
                                                     'PARTIAL',
                                                     'FULL',
                                                     'UNLIMITED')
                    ]
                },
                'fixed_quantity': {
                    'tag': 'fixedQuantity',
                    'type': 'int',
                },
                'suite_identifier': {
                    'tag': 'suiteIdentifier',
                    'type': 'choice',
                    'class': SuiteIdentifier,
                },
                'product': {
                    'tag': 'product',
                    'type': 'sequence',
                    'class': Product,
                },
                'common_license_attributes': {
                    'tag': 'commonLicenseAttributes',
                    'type': 'sequence',
                    'class': CommonLicenseAttributes,
                },
                'activation_attributes': {
                    'tag': 'activationAttributes',
                    'type': 'sequence',
                    'class': ActivationAttributes,
                },
                'entitlement_extension': {
                    'tag': 'entitlementExtension',
                    'type': 'sequence',
                    'class': EntitlementExtension,
                },
                'custom_attribute': {
                    'tag': 'customAttribute',
                    'type': 'sequence',
                    'class': CustomAttribute,
                },
                'entitlement_item_attributes': {
                    'tag': 'entitlementItemAttributes',
                }
            }

        # Product Key
        _SCHEMA_ = {
            'id': {
                'tag': 'pkId',
            },
            'start_date': {
                'tag': 'startDate',
                'type': 'date',
            },
            'end_date': {
                'tag': 'endDate',
                'type': 'date',
            },
            'item': {
                'tag': 'Item',
                'type': 'sequence',
                'class': ProductKeyItem,
            },
        }

    @base.webservice_meta(omit_empty=True)
    class EntitlementAttributes(base.WebServiceObject):

        @base.webservice_meta(omit_empty=True)
        class AttributeGroup(base.WebServiceObject):

            @base.webservice_meta(omit_empty=True)
            class Attribute(base.WebServiceObject):
                _SCHEMA_ = {
                    'name': {
                        'tag': 'attributeName',
                        'required': True,
                    },
                    'value': {
                        'tag': 'attributeValue',
                    },
                }

            # AttributeGroup
            _SCHEMA_ = {
                'attribute': {
                    'tag': 'attribute',
                    'type': 'sequence',
                    'class': Attribute,
                },
                'name': {
                    'tag': 'groupName',
                },
                'subgroup_name': {
                    'tag': 'subGroupName',
                }
            }

        # EntitlementAttributes
        _SCHEMA_ = {
            'attribute_group': {
                'tag': 'attributeGroup',
                'type': 'sequence',
                'class': AttributeGroup,
            }
        }

    _SCHEMA_ = {
        'external_id': {
            'tag': 'externalId',
            'type': 'string',
        },
        'eid': {
            'tag': 'eId',
            'type': 'string',
        },
        'as_whole': {
            'tag': 'entitlementAsWhole',
            'default': False,
            'type': 'bool',
        },
        'type': {
            'tag': 'entitlementType',
            'type': 'string',
            'restrictions': [
                restrictions.EnumRestriction('PARENT', 'TRANSACTION'),
            ]
        },
        'linked_id': {
            'tag': 'linkedEntId',
            'type': 'string',
        },
        'revision': {
            'tag': 'revision',
            'type': 'string',
        },
        'start_date': {
            'tag': 'startDate',
            'type': 'date',
        },
        'end_date': {
            'tag': 'endDate',
            'type': 'date',
        },
        'customer_identifier': {
            'tag': 'customerIdentifier',
            'type': 'choice',
            'class': CustomerIdentifier,
        },
        'contact_identifier': {
            'tag': 'contactIdentifier',
            'type': 'choice',
            'class': ContactIdentifier,
        },
        'channel_partner_identifier': {
            'tag': 'channelPartnerIdentifier',
            'type': 'choice',
            'class': ChannelPartnerIdentifier,
        },
        'user_registration': {
            'tag': 'userRegistration',
            'type': 'string',
            'restrictions': [
                restrictions.EnumRestriction('NONE', 'OPTIONAL', 'MANDATORY'),
            ]
        },
        'ref1': {
            'tag': 'refId1',
            'type': 'string',
        },
        'ref2': {
            'tag': 'refId2',
            'type': 'string',
        },
        'activation_allowed': {
            'tag': 'activationAllowed',
            'type': 'bool',
            'default': True,
        },
        'revocation_allowed': {
            'tag': 'revocationAllowed',
            'type': 'bool',
            'default': True,
        },
        'lifecycle_stage': {
            'tag': 'lifeCycleStage',
            'type': 'string',
            'restrictions': [
                restrictions.EnumRestriction('DRAFT', 'COMMITTED'),
            ],
        },
        'action': {
            'tag': 'action',
            'type': 'string',
            'restrictions': [
                restrictions.EnumRestriction('UPDATE',
                                             'COMMIT',
                                             'RENEWLICENSE',
                                             'CLOSE',
                                             'DISABLE'),
            ]
        },
        'send_notification': {
            'tag': 'sendNotifcation',
            'type': 'bool',
        },
        'cc_email': {
            'tag': 'ccEmail',
            'type': 'string',
        },
        'is_test': {
            'tag': 'isTest',
            'type': 'bool',
        },
        'custom_attribute': {
            'tag': 'customAttribute',
            'type': 'sequence',
            'class': CustomAttribute,
        },
        'txn_history': {
            'tag': 'txnHistory',
            'type': 'sequence',
            'class': TxnHistory,
        },
        'product_key': {
            'tag': 'productKey',
            'type': 'sequence',
            'class': ProductKey,
        },
        'attributes': {
            'tag': 'entitlementAttributes',
            'type': 'sequence',
            'class': EntitlementAttributes,
        },
    }

    @classmethod
    def create(cls, start_date, end_date, num_activations, products,
               customer_id, contact_id, cc_email=None, ref1=None, ref2=None,
               user_registration='OPTIONAL', send_notification=True,
               type_='PARENT', as_whole=False):

        ent = cls()
        ent.start_date = start_date
        ent.end_date = end_date
        ent.ref1 = ref1
        ent.ref2 = ref2
        ent.send_notification = send_notification
        ent.cc_email = cc_email
        ent.type = type_
        ent.as_whole = as_whole
        ent.lifecycle_stage = 'DRAFT'
        ent.customer_identifier = ent.CustomerIdentifier(id=customer_id)
        ent.contact_identifier = ent.ContactIdentifier(id=contact_id)
        ent.user_registration = user_registration

        product_keys = []
        for name, ver in six.iteritems(products):
            key = ent.ProductKey(start_date=start_date, end_date=end_date)
            item = key.ProductKeyItem()
            item.total_quantity = num_activations
            item.available_quantity = num_activations
            item.activation_method = 'PARTIAL'

            product = item.Product()
            identifier = product.ProductIdentifier()
            name_ver = identifier.ProductNameVersion(name=name, version=ver)

            identifier.name_version = name_ver
            product.identifier = identifier
            item.product = product
            key.item = item
            product_keys.append(key)

        ent.product_key = product_keys
        return ent
