from omnihash.omnihash import main
import unittest

import click
from click.testing import CliRunner


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
def test_empty():
    runner = CliRunner()
    result = runner.invoke(main)
    print(result.output)
    assert result.exit_code == 0


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
    result = runner.invoke(main, ['hashme', 'LICENSE'])
    assert result.exit_code == 0
    assert '941c986ff0f3e90543dc5e2a0687ee99b19bff67' in result.output


def test_omnihashf():
    runner = CliRunner()
    result = runner.invoke(main, 'Hi -f sha2 -f SHA5'.split())
    assert result.exit_code == 0
    out = """
  SHA224:                7d5104ff2cee331a4586337ea64ab6a188e2b26aecae87227105dae1
  SHA256:                3639efcd08abb273b1619e82e78c29a7df02c1051b1820e99fc395dcaa3326b8
  SHA512:                45ca55ccaa72b98b86c697fdf73fd364d4815a586f76cd326f1785bb816ff7f1f88b46fb8448b19356ee788eb7d300\
b9392709a289428070b5810d9b5c2d440d
"""
    assert result.output.endswith(out)

    result = runner.invoke(main, 'Hi -c -f sha2 -c -f ITU'.split())
    assert result.exit_code == 0
    out = """
  SHA224:                7d5104ff2cee331a4586337ea64ab6a188e2b26aecae87227105dae1
  SHA256:                3639efcd08abb273b1619e82e78c29a7df02c1051b1820e99fc395dcaa3326b8
  CRC-8-ITU:             0xbe
"""
    print(out)
    assert result.output.endswith(out)


def test_omnihashs():
    runner = CliRunner()
    result = runner.invoke(main, ['hashme', 'LICENSE', '-s'])
    assert result.exit_code == 0
    assert '0398ccd0f49298b10a3d76a47800d2ebecd49859' in result.output


def test_omnihashcrc():
    runner = CliRunner()
    result = runner.invoke(main, ['hashme', 'README.md', '-sc'])
    assert result.exit_code == 0
    print(result.output)
    assert 'fb78992e561929a6967d5328f49413fa99048d06' in result.output
    assert '5d20a7c38be78000' in result.output


def test_url():
    runner = CliRunner()
    result = runner.invoke(main, ['hashme', 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png', '-c'])    # noqa
    assert result.exit_code == 0
    print(result.output)
    assert '26f471f6ebe3b11557506f6ae96156e0a3852e5b' in result.output
    assert '809089' in result.output

    result = runner.invoke(main, ['hashme', 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png', '-sc'])  # noqa
    assert result.exit_code == 0
    print(result.output)
    assert 'b61bad1cb3dfad6258bef11b12361effebe597a8c80131cd2d6d07fce2206243' in result.output
    assert '20d9c2bbdbaf669b' in result.output


def test_json():
    runner = CliRunner()
    result = runner.invoke(main, ["correct horse battery staple", "-j", "-m", "9cc2"])
    assert result.exit_code == 0
    print(result.output)
    assert '"MD5": "9cc2ae8a1ba7a93da39b46fc1019c481"' in result.output

if __name__ == '__main__':
    unittest.main()
