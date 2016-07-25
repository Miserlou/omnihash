#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import hashlib
import os
import sha3

from pyblake2 import blake2b, blake2s

@click.command()
@click.argument('hashmes', nargs=-1)
@click.option('-s', is_flag=True, default=False, help="Hash input as string, even if there is a file with that name.")
@click.option('-v', is_flag=True, default=False, help="Show version and quit.")
def main(hashmes, s, v):
    """
    If there is a file at hashme, read and omnihash that file.
    Elif hashme is a string, omnihash that.
    """

    if v:
        import pkg_resources
        version = pkg_resources.require("omnihash")[0].version
        click.echo(version)
        return

    for hashme in hashmes:
        if os.path.exists(hashme) and not s:
            click.echo("Hashing file %s.." % hashme)
            with open(hashme, mode='rb') as f:
                hashme_data = f.read()
                hashme_data = hashme.encode('utf-8')
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
        s = sha3.SHA3224()
        s.update(hashme_data)
        echo('SHA3_224', s.hexdigest().decode("utf-8"))

        s = sha3.SHA3256()
        s.update(hashme_data)
        echo('SHA3_256', s.hexdigest().decode("utf-8"))

        s = sha3.SHA3384()
        s.update(hashme_data)
        echo('SHA3_384', s.hexdigest().decode("utf-8"))

        s = sha3.SHA3512()
        s.update(hashme_data)
        echo('SHA3_512', s.hexdigest().decode("utf-8"))

        # BLAKE
        b = blake2s()
        b.update(hashme_data)
        echo('BLAKE2s', b.hexdigest())
        
        b = blake2b()
        b.update(hashme_data)
        echo('BLAKE2b', b.hexdigest())

def echo(algo, digest):
    click.echo('%-*s%s' % (32, click.style(algo, fg='green') + ':', digest))

if __name__ == '__main__':
    main()