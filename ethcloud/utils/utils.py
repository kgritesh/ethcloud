# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division

import importlib
import os
import random
import string
import tempfile
from contextlib import contextmanager

import logging
import six
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


def any_one(*args):
    """
    Validates that only one of provided arguments are truthy
    """
    i = iter(args)
    return any(i) and not any(i)


def random_string(length, letters=None):
    letters = letters or string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))


def import_class(cls_path):
    """
    Imports a class from dotted path to the class
    """
    if not isinstance(cls_path, six.string_types):
        return cls_path

    # cls is a module path to string
    if '.' in cls_path:
        # Try to import.
        module_bits = cls_path.split('.')
        module_path, class_name = '.'.join(module_bits[:-1]), module_bits[-1]
        module = importlib.import_module(module_path)
    else:
        # We've got a bare class name here, which won't work (No AppCache
        # to rely on). Try to throw a useful error.
        raise ImportError("Rquires a Python-style path (<module.module.Class>) "
                          "to load given cls. Only given '%s'." % cls_path)

    cls = getattr(module, class_name, None)

    if cls is None:
        raise ImportError(
            "Module '{}' does not appear to have a class called '{}'.".format(
                module_path, class_name))

    return cls


class VerbosityFilter(object):

    def __init__(self, verbosity):
        self.verbosity = verbosity

    def filter(self, record):
        if self.verbosity < 0:
            return int(record.levelno >= logging.WARN)

        elif self.verbosity == 0:
            return int(record.levelno >= logging.INFO)

        return 1
