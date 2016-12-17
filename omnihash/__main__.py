#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import json
import omnihash
import sys

import click
import pkg_resources


class FileIter(object):
    """An iterator that chunks in bytes a file-descriptor, auto-closing it when exhausted."""
    def __init__(self, fd):
        self._fd = fd
        self._iter = iter(lambda: fd.read(io.DEFAULT_BUFFER_SIZE), b'')

    def __iter__(self):
        return self._iter

    def next(self):
        try:
            return self._iter.next()
        except StopIteration:
            self._fd.close()
            raise


##
# CLI
##

@click.command()
@click.argument('hashmes', nargs=-1)
@click.option('-s', is_flag=True, default=False, help="Hash input as string, even if there is a file with that name.")
@click.option('-v', is_flag=True, default=False, help="Show version and quit.")
@click.option('-c', is_flag=True, default=False, help="Calculate CRCs as well.")
@click.option('-f', is_flag=False, default=False, multiple=True,
              help=("Select a family of algorithms: "
                    "include only algos having TEXT in their names."
                    "Use it multiple times to select more families."))
@click.option('-x', is_flag=False, default=False, multiple=True,
              help=("Exclude a family of algorithms: "
                    "skip algos having TEXT in their names."
                    "Use it multiple times to exclude more families."))
@click.option('-m', is_flag=False, default=False, help="Match input string.")
@click.option('-j', is_flag=True, default=False, help="Output result in JSON format.")
@click.pass_context
def main(click_context, hashmes, s, v, c, f, x, m, j):
    """
    If there is a file at `hashme`, read and omnihash that.
    Otherwise, assume `hashme` is a string.
    """

    # Print version and quit
    if v:
        version = pkg_resources.require("omnihash")[0].version
        click.echo(version)
        return

    m = m and m.lower()
    digfacts = omnihash.collect_digester_factories(f, x, c)

    results = []
    if not hashmes:
        # If no stdin, just help and quit.
        if not sys.stdin.isatty():
            stdin = click.get_binary_stream('stdin')
            bytechunks = iter(lambda: stdin.read(io.DEFAULT_BUFFER_SIZE), b'')
            if not j:
                click.echo("Hashing " + click.style("standard input", bold=True) + "..", err=True)
            results.append([omnihash.produce_hashes(None, bytechunks, digfacts, match=m, use_json=j)])
        else:
            print(click_context.get_help())
            return
    else:
        hash_many = len(hashmes) > 1
        for hashme in hashmes:
            result = {}
            data = omnihash.iterate_bytechunks(hashme, s, j, hash_many)
            if data:
                length, bytechunks = data
                result = omnihash.produce_hashes(length, bytechunks, digfacts, match=m, use_json=j)
            if result:
                result['NAME'] = hashme
                results.append(result)

    if results and j:
        print(json.dumps(results, indent=4, sort_keys=True))

##
# Entrypoint
##

if __name__ == '__main__':
    try:
        main()
    except ValueError as ex:
        click.echo(ex, err=True)
