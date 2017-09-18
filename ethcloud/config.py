# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division

from enum import Enum


class CloudProvider(Enum):
    AWS = 'AWS'


class Verbosity(Enum):
    SILENT = 0
    ERROR = 1
    WARN = 2
    INFO = 3
    DEBUG = 4
    DETAIL = 5


class EtherNetwork(Enum):
    FRONTIER = 1
    MORDEN = 2
    ROPSTEN = 3
    RINKEBY = 4

default_config = {
    'provider': CloudProvider.AWS,
    'verbosity': Verbosity.INFO,
    'network_port': 30303,
    'network': EtherNetwork.ROPSTEN,
    'node_name': 'geth-node',
    'cache': 128
}