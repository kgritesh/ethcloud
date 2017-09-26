# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from abc import ABCMeta

import six
from attrdict import AttrDict

from ethcloud import constants
from ethcloud.errors import ProviderNotSupported
from ethcloud.utils import utils


@six.add_metaclass(ABCMeta)
class CloudProvider(object):
    SUPPORTED_PROVIDERS = {
        'aws': 'ethcloud.provider.aws.AWSCloudProvider'
    }

    DEFAULT_REQUIRED = ['instance_name', 'remote_user']

    DEFAULT_CONFIG = None

    @classmethod
    def get(cls, config, logger):
        provider_name = config['provider']
        if provider_name not in cls.SUPPORTED_PROVIDERS:
            raise ProviderNotSupported(provider_name)

        module = cls.SUPPORTED_PROVIDERS[provider_name]
        provider_cls = utils.import_class(module)
        return provider_cls(config, logger)

    def __init__(self, config, logger):
        default_config = self._load_default_config()
        provider_config = config.pop('config')
        config_dict = {}

        for cf in [default_config, config, provider_config]:
            config_dict.update(cf)

        self.config = AttrDict(config_dict)
        self.logger = logger

    def get_instance(self):
        raise NotImplemented()

    def get_public_ip(self):
        raise NotImplemented()

    def validate_launch(self, *client_options):
        raise NotImplemented()

    def _load_default_config(self):
        config_path = os.path.join(constants.PROVISION_DIR, 'vars', self.DEFAULT_CONFIG)
        return utils.load_config_file(config_path)
