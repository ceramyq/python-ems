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


@six.add_metaclass(base.WebServiceMeta)
class Entitlement(base.WebServiceObject):

    @six.add_metaclass(base.WebServiceMeta)
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

    @six.add_metaclass(base.WebServiceMeta)
    class ContactIdentifier(base.WebServiceObject):
        _SCHEMA_ = {
            'id': {
                'tag': 'customerId',
                'type': 'int',
            },
            'email': {
                'tag': 'emailId',
            }
        }

    @six.add_metaclass(base.WebServiceMeta)
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

    @six.add_metaclass(base.WebServiceMeta)
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

    @six.add_metaclass(base.WebServiceMeta)
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

    @six.add_metaclass(base.WebServiceMeta)
    class ProductKey(base.WebServiceObject):

        @six.add_metaclass(base.WebServiceMeta)
        class ProductKeyItem(base.WebServiceObject):

            @six.add_metaclass(base.WebServiceMeta)
            class EnforcementIdentifier(base.WebServiceObject):
                # EnforcementIdentifier
                _SCHEMA_ = {
                    'name': {
                        'tag': 'enforcementName',
                    },
                    'version': {
                        'tag': 'enforcementVersion',
                        'type': 'float',
                    }
                }

            @six.add_metaclass(base.WebServiceMeta)
            class SuiteIdentifier(base.WebServiceObject):

                @six.add_metaclass(base.WebServiceMeta)
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

            @six.add_metaclass(base.WebServiceMeta)
            class Product(base.WebServiceObject):

                @six.add_metaclass(base.WebServiceMeta)
                class ProductIdentifier(base.WebServiceObject):

                    @six.add_metaclass(base.WebServiceMeta)
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
                            'tag': 'ProductNameVersion',
                            'type': 'sequence',
                            'class': ProductNameVersion,
                        }
                    }

                @six.add_metaclass(base.WebServiceMeta)
                class Feature(base.WebServiceObject):

                    @six.add_metaclass(base.WebServiceMeta)
                    class FeatureIdentifier(base.WebServiceObject):

                        @six.add_metaclass(base.WebServiceMeta)
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
                                'type': 'int',
                            },
                            'name_version': {
                                'tag': 'FeatureNameVersion',
                                'type': 'sequence',
                                'class': FeatureNameVersion,
                            }
                        }

                    @six.add_metaclass(base.WebServiceMeta)
                    class LicenseModel(base.WebServiceObject):

                        @six.add_metaclass(base.WebServiceMeta)
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

                        @six.add_metaclass(base.WebServiceMeta)
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

            @six.add_metaclass(base.WebServiceMeta)
            class CommonLicenseAttributes(base.WebServiceObject):

                @six.add_metaclass(base.WebServiceMeta)
                class Attribute(base.WebServiceObject):
                    # Attribute
                    _SCHEMA_ = {
                        'name': {
                            'tag': 'attributeName',
                            'required': True,
                        },
                        'value': {
                            'tag': 'attributeValue',
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

            @six.add_metaclass(base.WebServiceMeta)
            class ActivationAttributes(base.WebServiceObject):
                # ActivationAttributes
                _SCHEMA_ = {
                    'name': {
                        'tag': 'attributeName',

                    }
                }

            @six.add_metaclass(base.WebServiceMeta)
            class EntitlementExtension(base.WebServiceObject):
                # EntitlementExtension
                _SCHEMA_ = {

                }

            @six.add_metaclass(base.WebServiceMeta)
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

    @six.add_metaclass(base.WebServiceMeta)
    class EntitlementAttributes(base.WebServiceObject):

        @six.add_metaclass(base.WebServiceMeta)
        class AttributeGroup(base.WebServiceObject):

            @six.add_metaclass(base.WebServiceMeta)
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

    _META_ = {
        'tag': 'entitlement',
        'omit_empty': True,
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
            'tag': 'sendNotification',
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
