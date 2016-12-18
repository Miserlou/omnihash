#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import pkg_resources

import functools as fnt


##
# Plugins
##
PLUGIN_GROUP_NAME = 'omnihash.plugins'


def append_plugin_digesters(digfacts, plugin_group_name=PLUGIN_GROUP_NAME):
    """Plugin-loaders accept a :class:`DigesterFactories` instance to register their factory-funcs. """
    entry_points = pkg_resources.working_set.iter_entry_points(plugin_group_name)
    entry_points = sorted(entry_points, key=lambda ep: ep.name)
    for ep in entry_points:
        try:
            plugin_loader = ep.load()
            if callable(plugin_loader):
                plugin_loader(digfacts)
        except pkg_resources.DistributionNotFound as ex:
            pass
        except Exception as ex:
            click.echo('Failed LOADING plugin(%r@%s) due to: %s' % (
                       ep, ep.dist, ex), err=1)


def plugin_crc_digesters(digfacts):
    import crcmod.predefined as crcmod

    def ensure_crc_prefix(name):
        name = name.upper()
        if not name.startswith('CRC-'):
            name = 'CRC-%s' % name
        return name

    def digester_fact(crc_name, fsize):
        # A factory that ignores the `fsize` arg.
        return crcmod.PredefinedCrc(crc_name)

    algo_pairs = sorted(ensure_crc_prefix(rec[0]) for rec in crcmod._crc_definitions_table)
    digfacts.update((algo, fnt.partial(digester_fact, algo))
                    for algo in algo_pairs
                    if digfacts.is_algo_accepted(algo))


def plugin_sha3_digesters(digfacts):
    import sha3  # @UnresolvedImport because it is optional.

    def digester_fact(algo_class, fsize):
        # A factory that ignores the `fsize` arg.
        return algo_class()

    algo_pairs = ((algo.name.upper(), algo) for algo in (sha3.SHA3224, sha3.SHA3256, sha3.SHA3384, sha3.SHA3512))
    digfacts.update((algo, fnt.partial(digester_fact, cls))
                    for algo, cls in algo_pairs
                    if digfacts.is_algo_accepted(algo))


def plugin_pyblake2_digesters(digfacts):
    import pyblake2  # @UnresolvedImport because it is optional.

    def digester_fact(algo_class, fsize):
        # A factory that ignores the `fsize` arg.
        return algo_class()

    algo_pairs = zip(('BLAKE2S', 'BLAKE2B'), (pyblake2.blake2s, pyblake2.blake2b))
    digfacts.update((algo, fnt.partial(digester_fact, cls))
                    for algo, cls in algo_pairs
                    if digfacts.is_algo_accepted(algo))
