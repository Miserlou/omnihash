#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Standard Imports
from collections import OrderedDict

import click
import pkg_resources


##
# Plugins
##
PLUGIN_GROUP_NAME = 'omnihash.plugins'

known_digesters = OrderedDict()
""" Plugins add here 2-tuples (digester-factory-func, final-hashing-func). """


def intialize_plugins(plugin_group_name=PLUGIN_GROUP_NAME):
    entry_points = pkg_resources.working_set.iter_entry_points(plugin_group_name)
    entry_points = sorted(entry_points, key=lambda ep: ep.name)
    for ep in entry_points:
        try:
            plugin_loader = ep.load()
            if callable(plugin_loader):
                plugin_loader()
        except pkg_resources.DistributionNotFound as ex:
            pass
        except Exception as ex:
            click.echo('Failed LOADING plugin(%r@%s) due to: %s' % (
                       ep, ep.dist, ex), err=1)


# Plugin algos
def plugin_sha3_digesters():
    import sha3  # @UnresolvedImport

    known_digesters['SHA3_224'] = (sha3.SHA3224(), lambda d: d.hexdigest().decode("utf-8"))
    known_digesters['SHA3_256'] = (sha3.SHA3256(), lambda d: d.hexdigest().decode("utf-8"))
    known_digesters['SHA3_384'] = (sha3.SHA3384(), lambda d: d.hexdigest().decode("utf-8"))
    known_digesters['SHA3_512'] = (sha3.SHA3512(), lambda d: d.hexdigest().decode("utf-8"))


def plugin_pyblake2_digesters():
    import pyblake2  # @UnresolvedImport

    known_digesters['BLAKE2s'] = (pyblake2.blake2s(), lambda d: d.hexdigest())
    known_digesters['BLAKE2b'] = (pyblake2.blake2b(), lambda d: d.hexdigest())
