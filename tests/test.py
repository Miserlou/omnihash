import glob
import os
import re
import string
import sys
import unittest

import nose
from nose import case
from nose.pyversion import unbound_method
from nose import util

import click
from click.testing import CliRunner

from omnihash.omnihash import main

# Sanity
def test_hello_world():
    @click.command()
    @click.argument('name')
    def hello(name):
        click.echo('Hello %s!' % name)

    runner = CliRunner()
    result = runner.invoke(hello, ['Peter'])
    assert result.exit_code == 0
    assert result.output == 'Hello Peter!\n'

# Main
def test_omnihash():
    runner = CliRunner()
    result = runner.invoke(main, ['hashme'])
    print(result.output)
    assert result.exit_code == 0
    assert 'fb78992e561929a6967d5328f49413fa99048d06' in result.output

def test_omnihash2():
    runner = CliRunner()
    result = runner.invoke(main, ['hashme', 'asdf'])
    assert result.exit_code == 0
    assert 'fb78992e561929a6967d5328f49413fa99048d06' in result.output

def test_omnihashfile():
    runner = CliRunner()
    result = runner.invoke(main, ['hashme', 'README.md'])
    assert result.exit_code == 0
    assert 'fb78992e561929a6967d5328f49413fa99048d06' in result.output

def test_omnihashs():
    runner = CliRunner()
    result = runner.invoke(main, ['hashme', 'README.md', '-s'])
    assert result.exit_code == 0
    assert 'fb78992e561929a6967d5328f49413fa99048d06' in result.output

def test_omnihashcrc():
    runner = CliRunner()
    result = runner.invoke(main, ['hashme', 'README.md', '-sc'])
    assert result.exit_code == 0
    print(result.output)
    assert 'fb78992e561929a6967d5328f49413fa99048d06' in result.output
    assert '5d20a7c38be78000' in result.output

def test_url():
    runner = CliRunner()
    result = runner.invoke(main, ['hashme', 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png', '-c'])
    assert result.exit_code == 0
    print(result.output)
    assert '26f471f6ebe3b11557506f6ae96156e0a3852e5b' in result.output
    assert '809089' in result.output
    
    result = runner.invoke(main, ['hashme', 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png', '-sc'])
    assert result.exit_code == 0
    print(result.output)
    assert 'b61bad1cb3dfad6258bef11b12361effebe597a8c80131cd2d6d07fce2206243' in result.output
    assert '20d9c2bbdbaf669b' in result.output

if __name__ == '__main__':
    unittest.main()
