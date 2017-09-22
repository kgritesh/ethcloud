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


@cli.command()
@common_options
@click.option('--delete-iam-role', is_flag=True,
              help="Applicable for AWS Provider: Delete the ethereum client role")
@click.option('--delete-security-group', is_flag=True,
              help="Applicable for AWS Provider: Delete the ethereum client security group")
def delete(cloud_config, verbose, quiet, delete_iam_role=False,
           delete_security_group=False):
    """
    Delet an existing cloud instance running ethereum client
    """
    verbosity = -1 if quiet else verbose
    engine = Engine(cloud_config_file=cloud_config, verbosity=verbosity)
    engine.delete(delete_iam_role=delete_iam_role,
                  delete_security_group=delete_security_group)


if __name__ == '__main__':
    cli(default_map={
        'launch': {
            'auto_envvar_prefix': 'ETHCLOUD'
        }
    })
