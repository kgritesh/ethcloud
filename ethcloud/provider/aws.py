# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import boto3

from decorators import required_config
from errors import DuplicateNode, ClientNotFound
from provider.base import CloudProvider


class AWSCloudProvider(CloudProvider):
    DEFAULT_CONFIG = 'aws.yml'

    DEFAULT_REQUIRED = ['instance_name', 'aws_region']

    def get_instance(self):
        ec2 = boto3.resource('ec2', region_name=self.config['aws_region'])
        instances = list(
            ec2.instances.filter(Filters=[{
                'Name': 'tag:Identifier',
                'Values': [self.config.instance_name]
            }, {
                'Name': 'instance-state-name',
                'Values': ['running']
            }]).all()
        )

        return None if not instances else instances[0]

    def get_public_ip(self):
        instance = self.get_instance()
        if not instance:
            raise ClientNotFound(self.config.ec2_instance_name)
        return instance.public_ip_address

    @required_config('ec2_instance_type', 'aws_key')
    def validate_launch(self, *client_options):
        if self.get_instance():
            raise DuplicateNode(self.config.ec2_instance_name)
        return True
