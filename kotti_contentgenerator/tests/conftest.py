# -*- coding: utf-8 -*-

"""
Created on 2015-02-22
:author: Tiberiu Ichim (tiberiu.ichim@gmail.com)
"""

from pytest import fixture

pytest_plugins = "kotti"


@fixture(scope='session')
def custom_settings():
    return {}
