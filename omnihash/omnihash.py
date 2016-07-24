#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import hashlib
import os

@click.command()
@click.argument('hashme')
def main(hashme):
    """
    If there is a file at hashme, read and omnihash that file.
    Elif hashme is a string, omnihash that.
    """

    if os.path.exists(hashme):
        click.echo("Hashing file %s.." % hashme)
        with open(hashme, mode='rb') as f:
            hashme_data = f.read()
    else:
        click.echo("Hashing string '%s'.." % hashme)
        hashme_data = hashme

    done = []
    for algo in sorted(hashlib.algorithms_available):

        # algorithms_available can have duplicates
        if algo.upper() in done:
            continue
            
        h = hashlib.new(algo)
        h.update(hashme_data)
        click.echo('%-*s%s' % (32, click.style(algo, fg='green') + ':', h.hexdigest()))
        done.append(algo)

if __name__ == '__main__':
    main()