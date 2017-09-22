# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import click

# Hack becaue the module name is __main__ and not ethcloud.
from constants import VERSION
from core import Engine


@click.group()
@click.version_option(VERSION, prog_name="ethcloud")
def cli():
    """
    A tool to launch and interface with a ethereum client running on a remote instance
    """
    pass


config_option = click.option('-c', '--cloud-config', required=True,
                             type=click.Path(exists=True, resolve_path=True),
                             help="Path to the cloud config to use to launch")


def common_options(fn):
    common_opts = [
        config_option,
        click.option('-v', '--verbose', count=True,
                     help="verbose mode or level (support upto 4 levels)"),
        click.option('-q', '--quiet', is_flag=True,
                     help="Only log errors and warnings"),
    ]

    for opt in reversed(common_opts):
        fn = opt(fn)

    return fn


@cli.command(context_settings=dict(
     ignore_unknown_options=True,
     allow_extra_args=True
))
@click.pass_context
@common_options
def launch(ctx, cloud_config, verbose, quiet):
    """
    Launch a new instance in the cloud and start a ethereum client on the instance
    """
    verbosity = -1 if quiet else verbose
    engine = Engine(cloud_config_file=cloud_config, verbosity=verbosity)
    engine.launch(*ctx.args)


@cli.command(context_settings=dict(
     ignore_unknown_options=True,
     allow_extra_args=True
))
@click.pass_context
@common_options
def update(ctx, cloud_config, verbose, quiet):
    """
    Update an existing cloud instance running ethereum client
    """
    verbosity = -1 if quiet else verbose
    engine = Engine(cloud_config_file=cloud_config, verbosity=verbosity)
    engine.update_instance(*ctx.args)


@cli.command(context_settings=dict(
     ignore_unknown_options=True,
     allow_extra_args=True
))
@click.pass_context
@config_option
def logs(ctx, cloud_config):
    """
    Show ethereum client logs
    """
    engine = Engine(cloud_config_file=cloud_config)
    engine.logs(*ctx.args)


@cli.command()
@config_option
def attach(cloud_config):
    """
    Attach to geth console.
    """
    engine = Engine(cloud_config_file=cloud_config)
    engine.attach()


@cli.command()
@config_option
def stop(cloud_config):
    """
    Stop geth ethereum client without destroying the instance
    """
    engine = Engine(cloud_config_file=cloud_config)
    engine.stop()


@cli.command(context_settings=dict(
     ignore_unknown_options=True,
     allow_extra_args=True
))
@click.pass_context
@config_option
def start(ctx, cloud_config):
    """
    Restart Ethereum Client with updated config
    """
    engine = Engine(cloud_config_file=cloud_config)
    engine.start(*ctx.args)



# @cli.command()
# @click.option('--aws-region', type=click.STRING,
#               help="Region where new geth instance must be launched")
# @click.option('--aws-key', type=click.STRING,
#               help="AWS Key to be used for default user. ")
# @click.option('--ec2-ami-id', type=click.STRING,
#               help="AMI to be used to create a new instance")
# @click.option('--ec2-instance-type', type=click.STRING,
#               help="EC2 Instance type to be created")
# @click.option('--ec2-volume-size', type=click.INT,
#               help="Size(GB) of EBS Volume to be attached with the instance")
# @click.option('--aws-config',
#               type=click.Path(exists=True, resolve_path=True),
#               help="Load aws config from a .yaml file")
# @click.option('--geth-opts',
#               type=click.STRING,
#               help="Set of options to be used to launch ethereum client")
# @click.option('-v', '--verbose', count=True)
# @click.option('--ec2-instance-name',
#               type=click.STRING,
#               help="Name/Identifier for the node")
# def launch(aws_region=None, aws_key=None, ec2_ami_id=None,
#            ec2_instance_type=None, ec2_volume_size=None, aws_config=None,
#            geth_opts=None, ec2_instance_name=None, verbose=0):
#
#     if aws_config and \
#             any((k is not None for k in
#                  (aws_region, aws_key, ec2_ami_id, ec2_volume_size, geth_opts))):
#         raise click.UsageError('If configuration file is passed then no other '
#                                'configuration should not be set')
#
#     pr = Provisioner(aws_region=aws_region, aws_key=aws_key,
#                      ec2_instance_type=ec2_instance_type,
#                      ec2_ami_id=ec2_ami_id,  ec2_volume_size=ec2_volume_size,
#                      aws_config=aws_config, geth_opts=geth_opts,
#                      ec2_instance_name=ec2_instance_name,
#                      verbosity=verbose)
#
#     pr.run()
#
#
# @cli.command(context_settings=dict(
#     ignore_unknown_options=True,
#     allow_extra_args=True
# ))
# @pass_context
# @click.option('--aws-region', type=click.STRING,
#               prompt=True,
#               help="Region where new geth instance must be launched")
# @click.option('--ec2-instance-name',
#               type=click.STRING,
#               prompt=True,
#               help="Name/Identifier for the node")
# @click.option('--remote-user',
#               type=click.STRING,
#               default="ubuntu",
#               help="Default user on the remote system")
# def logs(ctx, aws_region, ec2_instance_name, remote_user):
#     client = GethClient(aws_region=aws_region, ec2_instance_name=ec2_instance_name,
#                         remote_user=remote_user)
#     return client.logs(*ctx.args)
#
#
# @cli.command()
# @click.option('--aws-region', type=click.STRING,
#               prompt=True,
#               help="Region where new geth instance must be launched")
# @click.option('--ec2-instance-name',
#               type=click.STRING,
#               prompt=True,
#               help="Name/Identifier for the node")
# @click.option('--remote-user',
#               type=click.STRING,
#               default="ubuntu",
#               help="Default user on the remote system")
# def attach(aws_region, ec2_instance_name, remote_user):
#     client = GethClient(aws_region=aws_region, ec2_instance_name=ec2_instance_name,
#                         remote_user=remote_user)
#     return client.attach()
#
#
# @cli.command()
# @click.option('--aws-region', type=click.STRING,
#               prompt=True,
#               help="Region where new geth instance must be launched")
# @click.option('--ec2-instance-name',
#               type=click.STRING,
#               prompt=True,
#               help="Name/Identifier for the node")
# @click.option('--remote-user',
#               type=click.STRING,
#               default="ubuntu",
#               help="Default user on the remote system")
# def stop(aws_region, ec2_instance_name, remote_user):
#     client = GethClient(aws_region=aws_region, ec2_instance_name=ec2_instance_name,
#                         remote_user=remote_user)
#     return client.stop()
#
#
# @cli.command()
# @click.argument('command', type=click.STRING)
# @click.option('--aws-region', type=click.STRING,
#               prompt=True,
#               help="Region where new geth instance must be launched")
# @click.option('--ec2-instance-name',
#               type=click.STRING,
#               prompt=True,
#               help="Name/Identifier for the node")
# @click.option('--remote-user',
#               type=click.STRING,
#               default="ubuntu",
#               help="Default user on the remote system")
# def account(command, aws_region, ec2_instance_name, remote_user):
#     client = GethClient(aws_region=aws_region, ec2_instance_name=ec2_instance_name,
#                         remote_user=remote_user)
#     return client.account(command)


if __name__ == '__main__':
    cli(default_map={
        'launch': {
            'auto_envvar_prefix': 'ETHCLOUD'
        }
    })
