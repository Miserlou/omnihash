#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import crcmod.predefined
import hashlib
import os
import requests
import sha3
import validators
import zlib

from pyblake2 import blake2b, blake2s

@click.command()
@click.argument('hashmes', nargs=-1)
@click.option('-s', is_flag=True, default=False, help="Hash input as string, even if there is a file with that name.")
@click.option('-v', is_flag=True, default=False, help="Show version and quit.")
@click.option('-c', is_flag=True, default=False, help="Calculate CRCs as well.")
def main(hashmes, s, v, c):
    """
    If there is a file at hashme, read and omnihash that file.
    Elif hashme is a string, omnihash that.
    """

    # Print version and quit
    if v:
        import pkg_resources
        version = pkg_resources.require("omnihash")[0].version
        click.echo(version)
        return

    for hashme in hashmes:
        # URL
        if not s and validators.url(hashme):
            click.echo("Hashing content of URL '%s'.." % hashme)
            try:
                response = requests.get(hashme)
            except requests.exceptions.ConnectionError as e:
                print ("Not a valid URL. :(")
                continue
            except Exception as e:
                print ("Not a valid URL. %s" % e)
                continue                
            if response.status_code != 200:
                click.echo("Response returned %s. :(" % response.status_code)
                continue
            hashme_data = response.content
        # File
        elif os.path.exists(hashme) and not s:
            click.echo("Hashing file %s.." % hashme)
            with open(hashme, mode='rb') as f:
                hashme_data = f.read()
                hashme_data = hashme_data.encode('utf-8')
        # String
        else:
            click.echo("Hashing string '%s'.." % hashme)
            hashme_data = hashme.encode('utf-8')

        # Default Algos
        done = []
        for algo in sorted(hashlib.algorithms_available):

            # algorithms_available can have duplicates
            if algo.upper() in done:
                continue
                
            h = hashlib.new(algo)
            h.update(hashme_data)
            echo(algo, h.hexdigest())
            done.append(algo)

        # SHA3 Family
        sha = sha3.SHA3224()
        sha.update(hashme_data)
        echo('SHA3_224', sha.hexdigest().decode("utf-8"))

        sha = sha3.SHA3256()
        sha.update(hashme_data)
        echo('SHA3_256', sha.hexdigest().decode("utf-8"))

        sha = sha3.SHA3384()
        sha.update(hashme_data)
        echo('SHA3_384', sha.hexdigest().decode("utf-8"))

        sha = sha3.SHA3512()
        sha.update(hashme_data)
        echo('SHA3_512', sha.hexdigest().decode("utf-8"))

        # BLAKE
        blake = blake2s()
        blake.update(hashme_data)
        echo('BLAKE2s', blake.hexdigest())
        
        blake = blake2b()
        blake.update(hashme_data)
        echo('BLAKE2b', blake.hexdigest())

        # CRC
        if c:
            for name in sorted(crcmod.predefined._crc_definitions_by_name):
                crc_name = crcmod.predefined._crc_definitions_by_name[name]['name']
                crc_func = crcmod.predefined.mkCrcFun(crc_name)
                echo(crc_name.upper(), hex(crc_func(hashme_data)))


def echo(algo, digest):
    click.echo('%-*s%s' % (32, click.style(algo, fg='green') + ':', digest))

if __name__ == '__main__':
    main()
