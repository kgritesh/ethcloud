# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division

import json
import os
from subprocess import Popen

import sys
import yaml

from utils import utils

PROVISION_DIR = os.path.dirname(os.path.abspath(__file__))


class Provisioner:

    DEFAULT_CONFIG_FILE = os.path.join(PROVISION_DIR, 'default.yml')

    REQUIRED_PARAMS = ['aws_region', 'aws_key', 'ec2_instance_name',
                       'ec2_instance_type']

    def __init__(self, aws_config=None, **kwargs):

        self._load_config(aws_config)
        for key, value in kwargs.items():
            if value:
                self.config[key] = value
        self._validate_config()

    def _load_config(self, config_file=None):
        with open(self.DEFAULT_CONFIG_FILE, 'r') as fl:
            config = yaml.load(fl.read())

        if config_file:
            with open(config_file, 'r') as fl:
                config.update(yaml.load(fl.read()))

        config['cwd'] = PROVISION_DIR
        self.config = config

    def _validate_config(self):
        missing = [
            key for key in self.REQUIRED_PARAMS
            if not self.config.get(key, None)
        ]

        if missing:
            raise ValueError('Missing required parameters {}'.format(
                ', '.join(missing)
            ))

    def run(self):
        with utils.temporary_file(suffix='.json') as fl:
            fl.write(json.dumps(self.config).encode('utf-8'))
            fl.close()
            command = ['ansible-playbook', '-i', 'inventory', 'launch.yml',
                       '--extra-vars', '@{}'.format(fl.name)]

            if self.config.get('verbosity'):
                command.append('-{}'.format('v' * self.config['verbosity']))

            print ('Initiating a geth instance using ansible', command)
            process = Popen(command,
                            cwd=os.path.join(PROVISION_DIR, 'ansible'),
                            stdout=sys.stdout)
            process.communicate()

