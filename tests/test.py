from omnihash.omnihash import main
import os
import sys
import unittest

import click
from click.testing import CliRunner


class TOmnihash(unittest.TestCase):

    # Sanity
    def test_hello_world(self):
        @click.command()
        @click.argument('name')
        def hello(name):
            click.echo('Hello %s!' % name)

        runner = CliRunner()
        result = runner.invoke(hello, ['Peter'])
        self.assertEqual(result.exit_code, 0, result.exception)
        self.assertEqual(result.output, 'Hello Peter!\n')

    # Main
    def test_empty(self):
        runner = CliRunner()
        result = runner.invoke(main)
        print(result.output)
        self.assertEqual(result.exit_code, 0, result.exception)

    def test_omnihash(self):
        runner = CliRunner()
        result = runner.invoke(main, ['hashme'])
        print(result.output)
        self.assertEqual(result.exit_code, 0, result.exception)
        self.assertIn('fb78992e561929a6967d5328f49413fa99048d06', result.output)

    def test_omnihash2(self):
        runner = CliRunner()
        result = runner.invoke(main, ['hashme', 'asdf'])
        self.assertEqual(result.exit_code, 0, result.exception)
        self.assertIn('fb78992e561929a6967d5328f49413fa99048d06', result.output)

    def test_omnihashfile(self):
        runner = CliRunner()
        result = runner.invoke(main, ['hashme', 'LICENSE'])
        self.assertEqual(result.exit_code, 0, result.exception)
        #print(result.output)
        self.assertIn('941c986ff0f3e90543dc5e2a0687ee99b19bff67', result.output)

    def test_omnihashfile_conjecutive(self):
        import re
        runner = CliRunner()
        result = runner.invoke(main, 'LICENSE LICENSE -f sha1'.split())
        self.assertEqual(result.exit_code, 0, result.exception)
        #print(result.output)
        matches = re.findall('941c986ff0f3e90543dc5e2a0687ee99b19bff67', result.output)
        self.assertEqual(len(matches), 4)

    @unittest.skipIf(sys.version_info[0] < 3, "unittest has no `assertRegex()`.")
    def test_omnihashfile_length(self):
        runner = CliRunner()

        fpath = 'LICENSE'
        text = 'hashme'
        result = runner.invoke(main, [text, fpath])
        self.assertEqual(result.exit_code, 0, result.exception)
        self.assertRegex(result.output, r'LENGTH: +%i\D' % len(text))
        filelen = os.stat(fpath).st_size
        self.assertRegex(result.output, r'LENGTH: +%i\D' % filelen)

    @unittest.skipIf(sys.version_info[0] < 3, "unittest has no `assertRegex()`.")
    def test_omnihashfile_length_zero(self):
        runner = CliRunner()

        result = runner.invoke(main, [''])
        self.assertEqual(result.exit_code, 0, result.exception)
        self.assertRegex(result.output, r'LENGTH: +0\D')

    def test_omnihashf(self):
        runner = CliRunner()
        result = runner.invoke(main, 'Hi -f sha2 -f SHA5'.split())
        self.assertEqual(result.exit_code, 0, result.exception)
        out = """
  SHA224:                7d5104ff2cee331a4586337ea64ab6a188e2b26aecae87227105dae1
  SHA256:                3639efcd08abb273b1619e82e78c29a7df02c1051b1820e99fc395dcaa3326b8
  SHA512:                45ca55ccaa72b98b86c697fdf73fd364d4815a586f76cd326f1785bb816ff7f1f88b46fb8448b19356ee\
788eb7d300b9392709a289428070b5810d9b5c2d440d
"""
        assert result.output.endswith(out)

        result = runner.invoke(main, 'Hi -c -f sha2 -c -f ITU'.split())
        self.assertEqual(result.exit_code, 0, result.exception)
        out = """
  SHA224:                7d5104ff2cee331a4586337ea64ab6a188e2b26aecae87227105dae1
  SHA256:                3639efcd08abb273b1619e82e78c29a7df02c1051b1820e99fc395dcaa3326b8
  CRC-8-ITU:             0xbe
"""
        print(out)
        assert result.output.endswith(out)

    def test_omnihashs(self):
        runner = CliRunner()
        result = runner.invoke(main, ['hashme', 'LICENSE', '-s'])
        self.assertEqual(result.exit_code, 0, result.exception)
        self.assertIn('0398ccd0f49298b10a3d76a47800d2ebecd49859', result.output)

    def test_omnihashcrc(self):
        runner = CliRunner()
        result = runner.invoke(main, ['hashme', 'README.md', '-sc'])
        self.assertEqual(result.exit_code, 0, result.exception)
        print(result.output)
        self.assertIn('fb78992e561929a6967d5328f49413fa99048d06', result.output)
        self.assertIn('5d20a7c38be78000', result.output)

    def test_url(self):
        runner = CliRunner()
        result = runner.invoke(main, ['hashme', 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png', '-c'])    # noqa
        self.assertEqual(result.exit_code, 0, result.exception)
        print(result.output)
        self.assertIn('26f471f6ebe3b11557506f6ae96156e0a3852e5b', result.output)
        self.assertIn('809089', result.output)

        result = runner.invoke(main, ['hashme', 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png', '-sc'])  # noqa
        self.assertEqual(result.exit_code, 0, result.exception)
        print(result.output)
        self.assertIn('b61bad1cb3dfad6258bef11b12361effebe597a8c80131cd2d6d07fce2206243', result.output)
        self.assertIn('20d9c2bbdbaf669b', result.output)

    def test_json(self):
        runner = CliRunner()
        result = runner.invoke(main, ["correct horse battery staple", "-j", "-m", "9cc2"])
        self.assertEqual(result.exit_code, 0, result.exception)
        print(result.output)
        self.assertIn('"MD5": "9cc2ae8a1ba7a93da39b46fc1019c481"', result.output)

    def test_omnihashfile_git(self):
        runner = CliRunner()
        result = runner.invoke(main, 'LICENSE -f git'.split())
        self.assertEqual(result.exit_code, 0, result.exception)
        #print(result.output)
        self.assertIn('3e108735fcf3efac2b181874a34861a9fb5e7cc1', result.output)
        self.assertIn('25063c5229e9e558e3207413a1fa56c6262eedc2', result.output)
        self.assertIn('2c97833c235648e752a00f8ef709fbe2f3523ca4', result.output)

if __name__ == '__main__':
    unittest.main()
