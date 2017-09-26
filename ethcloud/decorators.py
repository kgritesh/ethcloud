# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools

from .errors import MissingRequiredParams


def required_config(*params):
    """
    A decorator that ensures that provided params are present in the config
    """

    def decorator(fnc):
        @functools.wraps(fnc)
        def wrapper(provider, *args, **kwargs):
            required_params = provider.DEFAULT_REQUIRED + list(params)
            missing_params = list(
                filter(lambda p: provider.config.get(p) is None, required_params)
            )

            if not missing_params:
                return fnc(provider, *args, **kwargs)
            else:
                raise MissingRequiredParams(missing_params)

        return wrapper
    return decorator