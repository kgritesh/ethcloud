# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division


class NoClientFound(Exception):

    def __init__(self, ec2_instance_name):
        super('No ethereum node found with name: {}'.format(ec2_instance_name))
