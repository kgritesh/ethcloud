# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division


class ClientNotFound(Exception):

    def __init__(self, ec2_instance_name):
        super(ClientNotFound, self).__init__(
            'No ethereum node found with name: {}'.format(ec2_instance_name))


class ProviderNotSupported(Exception):
    def __init__(self, provider_name):
        super(ProviderNotSupported, self).__init__(
            'Provider: {} not supported yet'.format(provider_name)
        )


class MissingRequiredParams(Exception):

    def __init__(self, missing_params):
        super(MissingRequiredParams, self).__init__(
            'Missing required parameters: {}'.format(', '.join(missing_params))
        )


class DuplicateNode(Exception):
    def __init__(self, node_name):
        super(DuplicateNode, self).__init__(
            'An ethereum client node with {} already exists'.format(node_name)
        )
