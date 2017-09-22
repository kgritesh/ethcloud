# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os
from contextlib import contextmanager
from subprocess import Popen

import sys

import logging

import constants
from errors import ClientNotFound
from provider.base import CloudProvider
from utils import utils
from utils.utils import VerbosityFilter


class Engine(object):
    """
    This class actually provides functionality for all the commands that this
    tool supports.
    """

    DEFAULT_CONFIG = 'defaults.yml'
    LOG_COMMAND = 'sudo journalctl -xeu geth'

    ATTACH_COMMAND = 'geth attach http://:8545'

    STOP_COMMAND = 'sudo systemctl stop geth'

    ACCOUNT_COMMAND = 'geth account {}'

    INVENTORY = """
        [ethereum_nodes]
        {}
    """

    def __init__(self, cloud_config_file=None, verbosity=0):
        """
        :param cloud_config_file: Optional Config file used while launching a new cloud instance
        :param verbosity: Level of verbosity required in logging
        """
        self.cloud_config_file = cloud_config_file
        self.verbosity = verbosity
        self.logger = logging.getLogger('ethcloud')
        self.logger.addFilter(VerbosityFilter(self.verbosity))
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.logger.setLevel(logging.DEBUG)
        self._load_provider()

    @property
    def config(self):
        return self.provider.config

    def _load_default_config(self):
        config_path = os.path.join(constants.PROVISION_DIR, 'vars', self.DEFAULT_CONFIG)
        return utils.load_config_file(config_path)

    def _load_provider(self):
        config = self._load_default_config()
        config.update(utils.load_config_file(self.cloud_config_file))
        config['provision_dir'] = constants.PROVISION_DIR
        self.provider = CloudProvider.get(config, self.logger)

    def update_client_options(self, client_options):
        self.provider.config['geth_opts'] = ' '.join(client_options)
        print('Geth Opts', self.provider.config['geth_opts'])

    def launch(self, *client_options):
        self.provider.validate_launch(*client_options)
        self.update_client_options(client_options)
        commands = ['ansible-playbook', '-i', 'inventory', 'launch.yml']
        self.logger.info('Launching a new node instance: {} on {}'.format(
            self.config.instance_name, self.config.provider
        ))
        return self._run_provision_command(commands)

    def update_instance(self, *args):
        with self._temporary_inventory() as tf:
            commands = ['ansible-playbook', '-i', tf.name, 'provision.yml']
            commands.extend(args)
            self.logger.info('Updating an existing instance: {} on {}'.format(
                self.config.instance_name, self.config.provider
            ))

            return self._run_provision_command(commands)

    def start(self, *client_options):
        self.update_client_options(client_options)
        self.update_instance('--tags', 'geth-systemd-config')

    def logs(self, *args):
        remote_command = '{} {}'.format(self.LOG_COMMAND, ' '.join(args))
        return self._run_ssh_command(remote_command)

    def attach(self):
        return self._run_ssh_command(self.ATTACH_COMMAND)

    def stop(self):
        return self._run_ssh_command(self.STOP_COMMAND)

    def delete(self, **kwargs):
        instance = self.provider.get_instance()
        if not instance:
            raise ClientNotFound(self.provider.config.instance_name)

        kwargs['delete_instance_ids'] = [instance.instance_id]
        self.provider.config.update(**kwargs)
        with self._temporary_inventory() as tf:
            commands = ['ansible-playbook', '-i', tf.name, 'delete.yml']
            self.logger.info('Delete an existing instance: {} on {}'.format(
                self.config.instance_name, self.config.provider
            ))

            return self._run_provision_command(commands)

    def account(self, command):
        return self._run_ssh_command(self.ACCOUNT_COMMAND.format(command))

    @contextmanager
    def _temporary_inventory(self):
        public_ip = self.provider.get_public_ip()
        with utils.temporary_file() as tf:
            tf.write(self.INVENTORY.format(public_ip).encode('utf-8'))
            tf.close()
            yield tf

    def _run_provision_command(self, commands):
        with utils.temporary_file(suffix='.json') as fl:
            fl.write(json.dumps(self.config).encode('utf-8'))
            fl.close()
            commands.extend(['--extra-vars', '@{}'.format(fl.name)])
            if self.verbosity:
                commands.append('-{}'.format('v' * self.verbosity))

            process = Popen(commands, cwd=constants.PROVISION_DIR, stdout=sys.stdout)
            return process.communicate()

    def _run_ssh_command(self, remote_command, shell=False):
        public_ip = self.provider.get_public_ip()
        commands = ['ssh', '{}@{}'.format(self.config.remote_user, public_ip),
                    '-o', 'StrictHostKeyChecking=no',
                    remote_command]
        process = Popen(commands, stdout=sys.stdout, shell=shell)
        return process.communicate()
