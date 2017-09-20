# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division

from subprocess import Popen

import boto3
import sys

from errors import NoClientFound


class GethClient:

    LOG_COMMAND = 'sudo journalctl -xeu geth'

    def __init__(self, ec2_instance_name, aws_region, remote_user):
        self.ec2_instance_name = ec2_instance_name
        self.aws_region = aws_region
        self.remote_user = remote_user

    def _get_public_ip(self):
        ec2 = boto3.resource('ec2', region_name=self.aws_region)
        instances = list(
            ec2.instances.filter(Filters=[{
                'Name': 'tag:Name',
                'Values': [self.ec2_instance_name]
            }, {
                'Name': 'instance-state-name',
                'Values': ['running']
            }]).all()
        )

        if not instances:
            raise NoClientFound(self.ec2_instance_name)

        return instances[0].public_ip_address

    def _run_ssh_command(self, remote_command):
        public_ip = self._get_public_ip()
        commands = ['ssh', '{}@{}'.format(self.remote_user, public_ip),
                    '-o', 'StrictHostKeyChecking=no',
                    remote_command]
        print(commands)
        process = Popen(commands, stdout=sys.stdout)
        return process.communicate()

    def logs(self, *args):
        remote_command = '{} {}'.format(self.LOG_COMMAND, ' '.join(args))
        return self._run_ssh_command(remote_command)