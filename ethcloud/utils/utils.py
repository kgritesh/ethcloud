# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division

import os
import tempfile
from contextlib import contextmanager

import yaml


def load_config_file(file_name):
    with open(file_name, 'r') as fl:
        return yaml.load(fl.read()) or {}


@contextmanager
def temporary_file(**kwargs):
    kwargs['delete'] = False
    fl = tempfile.NamedTemporaryFile(**kwargs)
    yield fl
    try:
        os.remove(fl.name)
    except:
        pass
