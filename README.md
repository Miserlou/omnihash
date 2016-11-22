![omnihash!](http://i.imgur.com/IAAI2ll.png)

# omnihash [![Build Status](https://travis-ci.org/Miserlou/omnihash.svg)](https://travis-ci.org/Miserlou/omnihash) [![PyPI](https://img.shields.io/pypi/v/omnihash.svg)](https://pypi.python.org/pypi/omnihash) [![Python 2](https://img.shields.io/badge/Python-2-brightgreen.svg)](https://pypi.python.org/pypi/omnihash/) [![Python 3](https://img.shields.io/badge/Python-3-brightgreen.svg)](https://pypi.python.org/pypi/omnihash/)

A tiny little tool to hash strings, files, input streams and network resources using various common hashing algorithms.

This is useful during reverse engineering when you know that _something_ is being hashed,
but you don't know what or how. It's kind of like the opposite of a [hash identifier](https://github.com/psypanda/hashID).

## Installation

To install omnihash, simply:

    pip install omnihash

To install with the SHA3 and Blake2 algorithm plugins:

    pip install omnihash[sha3,pyblake2]

Please note that on *Windows*, those two libraries do not yet exist (as of Aug 2016).

## Usage

For strings:

    $ omnihash "correct horse battery staple"
    Hashing string 'correct horse battery staple'..
      DSA:                   abf7aad6438836dbe526aa231abde2d0eef74d42
      DSA-SHA:               abf7aad6438836dbe526aa231abde2d0eef74d42
      MD4:                   131adffe1d8712c1b624ba62b5bcf3fd
      MD5:                   9cc2ae8a1ba7a93da39b46fc1019c481
      MDC2:                  b41edfd5e9cb278433a4a5c740898ffb
      RIPEMD160:             5e708aa85ae8b0d080837c50bd63634d584edc00
      SHA:                   99add446c4eed3772a92fabe3ab2c56fc2c9a26e
      SHA1:                  abf7aad6438836dbe526aa231abde2d0eef74d42
      SHA224:                636f080709f287ec5c5ea79442fc4bb914924cd5c6ca8ff84e3410c4
      SHA256:                c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a
      SHA384:                c24b92449c871f33bbbf1fc1989e5e1037cfa9a3dfdb17947f8172226181e7825ebb4c750763915835bf125a590e05ae
      SHA512:                be5ef7679d88ab9a9045f6267e55f5e5784b4b8cd764b5cd855a5244f91c626953cd46c43d7668873fd6efbd3b221249315580031963472a078781fe046e62ae
      dsaEncryption:         abf7aad6438836dbe526aa231abde2d0eef74d42
      dsaWithSHA:            abf7aad6438836dbe526aa231abde2d0eef74d42
      ecdsa-with-SHA1:       abf7aad6438836dbe526aa231abde2d0eef74d42
      whirlpool:             8c0e81ff1650da90c70a859319ba923b8807ad26af0940f8562fd62e75878eed13f434ba47860223ac55d92d91a169b3f9a1cbd4f10f3fca1b877088e5675891
      SHA3_224:              5ee454bfad2d1e25ba74884af244379d17bf50ef46dbe644e7587fc8
      SHA3_256:              af9ac3dac56b02f1ea017e7657a9bb7e1778274e31509f134f023e41a5953866
      SHA3_384:              5a1caac1441d4d002d6650f558b6bb10593095fe4664496b8f1665f239d923e69f95cbd141c5dcf833770542ff2322e8
      SHA3_512:              4b65d7b7acc886f9add07db3a5d42bf0032fe0109a1fd56f623c7093e8a59689f9246918a4f388034ddf393231eaba0742b3dc1840e4556270a729ce56098f35
      BLAKE2s:               239dd0a7e138f5fced884939c200b9ed35e092c17cd27f6049a5d0bda9fd7b8b
      BLAKE2b:               84793833af5cf79ef9548fd505dbb6633e54c1b4ec2c4f577c3a0ae41764e50ce8278ab8f6e0edd3e90ab6ef0914ff0e49329e0703ecc2fb7fdac12a4823fea7

And files:

    $ omnihash /etc/hosts
    Hashing file '/etc/hosts'..
      DSA:                   0ec93cf2b8000b5b339d0c5435251ad14f85b553
      DSA-SHA:               0ec93cf2b8000b5b339d0c5435251ad14f85b553
      MD4:                   226fb465616a070fd027f8a5db118561
      MD5:                   8efb3881814e54b95b030ff37012e22a
      MDC2:                  8df8bca5c8dbfc87e9c399aad2c326ac
      RIPEMD160:             f98ef6e7b10b8c4d7e0d129136f42f66163b8767
      SHA:                   2c8e7f4dade830ae6a4fdc6d20fd4a93b43bbbae
      SHA1:                  0ec93cf2b8000b5b339d0c5435251ad14f85b553
      SHA224:                43f81c9b4e15a835a0857ceba586239932210c718e8861b8235e4dff
      SHA256:                04f186e74288a10e09dfbf8a88d64a1f33c0e698aaa6b75cdb0ac3aba87d5644
      SHA384:                f7592a8db187f42957834132d964be00266a38b2b1bf5511bb7e636ae13822a4f858b386c11a77f680e34c49ca9cd8c1
      SHA512:                df9896fc36a18cd04c1a133c3a79a4783456a301b4380e9b30ebe56012708c373456681d6066ad7608f26cbcc147bd171cf57f1f9a6e977bf16295945e32047b
      dsaEncryption:         0ec93cf2b8000b5b339d0c5435251ad14f85b553
      dsaWithSHA:            0ec93cf2b8000b5b339d0c5435251ad14f85b553
      ecdsa-with-SHA1:       0ec93cf2b8000b5b339d0c5435251ad14f85b553
      whirlpool:             69f0d48f1e134a09dc6172953527c344465d759d02d0a3a932d6b97a57d2e0ca1fba324180a013e84a7e7cd912de1fb6e50deb15d05a56c27f8ec53d58c768c2
      SHA3_224:              2a8d5b60d3d6003c25516d110ebd53284d3c669a61e03a81cc756a26
      SHA3_256:              e40fa76654213ce8fb8e449f5659294fd3f3bb2fa461ff8678e7ea99d94cec1e
      SHA3_384:              9e8df099fd06ca136ff87c63b17cdd284eaa03558515c35053db41b116bb91419710b948e908e74edddc74ca9cd3b76f
      SHA3_512:              8158c2f4a2aab1e0abe63ec83711fe3343531f6683c89e5ff539cf8d29eb7bce931443646cd2704a9f1b901436741cc28d230bc58c5e98ed42b676fc15bfa354
      BLAKE2s:               e84408c7fac52f8436c4f3ba5e4e2abd038e4735a343de471f7c1dc548cd6ddf
      BLAKE2b:               2c23f27128614351712d3e2851c9c24763499512117ceb55b3f277863880767a11272ec5abe5527a9ae08cdea367264aa31b9160da148c00f732806200076954

And URLs:

    $ omnihash https://cryptome.org
    Hashing content of URL 'https://cryptome.org'..
      DSA:                   f63c8212d4769f2740306d30df6e56e4d773c412
      DSA-SHA:               f63c8212d4769f2740306d30df6e56e4d773c412
      MD4:                   2a61fd067f31bc161545e7e6eb08e31f
      MD5:                   12d4aca3c58007350edae822301d7d83
      MDC2:                  fe7acaffad747aa9ab644bd37314b916
      RIPEMD160:             1e7b92befcd56f70b90f7a6b5d6b3e8b8c56a3f9
      SHA:                   124876e226334bfadaf71c00e60f2e77551b140a
      SHA1:                  f63c8212d4769f2740306d30df6e56e4d773c412
      SHA224:                5af71e96da3d3383ddff0fa308bd7714f91af5873f17f7fa944aa5c0
      SHA256:                c320ec6af2dc3c1129e238e3d06653cbe6f01d5c791763db4b9dcabe169debc6
      SHA384:                0cf01cf20737f91c9736c924ab4cd2c503bfbb055ed630b5fa80d94b598e26a2376c739c4d195e464e2259c0cb4f6313
      SHA512:                c978e3544a6d4b11ed180463e6916ac562d3c90c007a107205e2f61118e2f3d032caf2053bd4ee0ab5c4a287279d0294dec4663ab2e3ed90e3e7312c2ae69abc
      dsaEncryption:         f63c8212d4769f2740306d30df6e56e4d773c412
      dsaWithSHA:            f63c8212d4769f2740306d30df6e56e4d773c412
      ecdsa-with-SHA1:       f63c8212d4769f2740306d30df6e56e4d773c412
      whirlpool:             c12d0362a5c30aa8848db7e6fd3f13d8bd5094201a89389c0ab24793dbee6733834d03362f6a960816abd450a900c016797996ac46e50af38bb02681054f30e7
      SHA3_224:              7bdb6efdc640a25a30dbbf51cc7f22e17f6c1963d871f89506292b35
      SHA3_256:              31cb08dadd163c309e7a551e7a8104ea5f935c1933c0e9a4005ee26809958766
      SHA3_384:              c2257da2c3352c4165acbd3ada334eb0034c0ee514da8609823eb537bd089d8ddde2ef63eead0867208f8c5d10f866b3
      SHA3_512:              bd36ece65851c5238882d3861343c980f58888cc0057a6ac808e20ef28ce2e8970d1123c88360c13064f3dbd332a10369df6b4be9483a9b8860b9d2156dd3e65
      BLAKE2s:               f4b0dd61772776ba04a4f0c94975a92acc41eb61ac2745e60b3adb7a08dc88d4
      BLAKE2b:               c1635df205326331b565959edb4b3b64a81a352ec594c869d35a2373ee8f1b8288e9135c0627b6cc44d54378a4b1f1fb39e124065644b7b9a62f57dd0e16e8ab2c23f27128614351712d3e2851c9c24763499512117ceb55b3f277863880767a11272ec5abe5527a9ae08cdea367264aa31b9160da148c00f732806200076954


## Advanced usage

You can also hash items from the standard input like so:

    $ cat my_large_file.bin | omnihash

You can pass multiple inputs at any time (ex, `omnihash *`).

You can force string-hashing (not falling-back to files) with `-s`.

You may limit the number of algorithms using the `-f` (*"family"*) option:

    $ oh Hi -f sha2 -f sha5
    SHA224:                7d5104ff2cee331a4586337ea64ab6a188e2b26aecae87227105dae1
    SHA256:                3639efcd08abb273b1619e82e78c29a7df02c1051b1820e99fc395dcaa3326b8
    SHA512:                45ca55ccaa72b98b86c697fdf73fd364d4815a586f76cd326f1785bb816ff7f1f88b46fb8448b19356ee788eb7d300b9392709a289428070b5810d9b5c2d440d

You can filter for string matches using `-m`, like so:

    $ omnihash "correct horse battery staple" -m 9cc2
    Hashing string correct horse battery staple..
    MD5:                   9cc2ae8a1ba7a93da39b46fc1019c481

You can output in machine readable JSON with `-j`, like so:

    $ omnihash "correct horse battery staple" -j -m 9cc2
    {
        "MD5": "9cc2ae8a1ba7a93da39b46fc1019c481"
    }

It's aliased so you can actually just call `oh` if you're as lazy as I am.

You can also see the value for various CRC checks by using `-c`:

    $ omnihash  "correct horse battery staple" -c
    Hashing string 'correct horse battery staple'..
      DSA:                   abf7aad6438836dbe526aa231abde2d0eef74d42
      DSA-SHA:               abf7aad6438836dbe526aa231abde2d0eef74d42
      MD4:                   131adffe1d8712c1b624ba62b5bcf3fd
      MD5:                   9cc2ae8a1ba7a93da39b46fc1019c481
      MDC2:                  b41edfd5e9cb278433a4a5c740898ffb
      RIPEMD160:             5e708aa85ae8b0d080837c50bd63634d584edc00
      SHA:                   99add446c4eed3772a92fabe3ab2c56fc2c9a26e
      SHA1:                  abf7aad6438836dbe526aa231abde2d0eef74d42
      SHA224:                636f080709f287ec5c5ea79442fc4bb914924cd5c6ca8ff84e3410c4
      SHA256:                c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a
      SHA384:                c24b92449c871f33bbbf1fc1989e5e1037cfa9a3dfdb17947f8172226181e7825ebb4c750763915835bf125a590e05ae
      SHA512:                be5ef7679d88ab9a9045f6267e55f5e5784b4b8cd764b5cd855a5244f91c626953cd46c43d7668873fd6efbd3b221249315580031963472a078781fe046e62ae
      dsaEncryption:         abf7aad6438836dbe526aa231abde2d0eef74d42
      dsaWithSHA:            abf7aad6438836dbe526aa231abde2d0eef74d42
      ecdsa-with-SHA1:       abf7aad6438836dbe526aa231abde2d0eef74d42
      whirlpool:             8c0e81ff1650da90c70a859319ba923b8807ad26af0940f8562fd62e75878eed13f434ba47860223ac55d92d91a169b3f9a1cbd4f10f3fca1b877088e5675891
      SHA3_224:              5ee454bfad2d1e25ba74884af244379d17bf50ef46dbe644e7587fc8
      SHA3_256:              af9ac3dac56b02f1ea017e7657a9bb7e1778274e31509f134f023e41a5953866
      SHA3_384:              5a1caac1441d4d002d6650f558b6bb10593095fe4664496b8f1665f239d923e69f95cbd141c5dcf833770542ff2322e8
      SHA3_512:              4b65d7b7acc886f9add07db3a5d42bf0032fe0109a1fd56f623c7093e8a59689f9246918a4f388034ddf393231eaba0742b3dc1840e4556270a729ce56098f35
      BLAKE2s:               239dd0a7e138f5fced884939c200b9ed35e092c17cd27f6049a5d0bda9fd7b8b
      BLAKE2b:               84793833af5cf79ef9548fd505dbb6633e54c1b4ec2c4f577c3a0ae41764e50ce8278ab8f6e0edd3e90ab6ef0914ff0e49329e0703ecc2fb7fdac12a4823fea7
      CRC-16:                0x72bc
      CRC-16-BUYPASS:        0xed6e
      CRC-16-DDS-110:        0x929c
      CRC-16-DECT:           0x73e5
      CRC-16-DNP:            0xfd30
      CRC-16-EN-13757:       0x2ae7
      CRC-16-GENIBUS:        0x493a
      CRC-16-MAXIM:          0x8d43
      CRC-16-MCRF4XX:        0xdbf8
      CRC-16-RIELLO:         0xb464
      CRC-16-T10-DIF:        0x2510
      CRC-16-TELEDISK:       0xdd3d
      CRC-16-USB:            0x67eb
      CRC-24:                0xbe455f
      CRC-24-FLEXRAY-A:      0xad0a8a
      CRC-24-FLEXRAY-B:      0x5d6e72
      CRC-32:                0xcb7e6e10L
      CRC-32-BZIP2:          0x8f6407fL
      CRC-32C:               0xbd9d695aL
      CRC-32D:               0xd42e1822L
      CRC-32-MPEG:           0xf709bf80L
      CRC-32Q:               0xafc633bfL
      CRC-64:                0x98aa19c00b783c4L
      CRC-64-JONES:          0xc1c681b1fee4d316L
      CRC-64-WE:             0x41097f04e906dfecL
      CRC-8:                 0xb9
      CRC-8-DARC:            0xe1
      CRC-8-I-CODE:          0x99
      CRC-8-ITU:             0xec
      CRC-8-MAXIM:           0xec
      CRC-8-ROHC:            0x31
      CRC-8-WCDMA:           0xd6
      CRC-AUG-CCITT:         0x301f
      CRC-CCITT-FALSE:       0xb6c5
      JAMCRC:                0x348191efL
      KERMIT:                0x22cd
      MODBUS:                0x9814
      POSIX:                 0x60e7b181L
      X-25:                  0x2407
      XFER:                  0x8648a5a9L
      XMODEM:                0x1a5a

More information can be found with `--help`.

## Extension plugins

You may extend the supported hashing algorithms using [*setuptools*'s extension machanism](https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins),
by crafting python ditributions (plugins) that attach to the `'omnihash.plugins' entry_point`.
Read the sources of this project as example, since the mechanism is already utilized for the "extras" dependencies.

### License

MIT license, 2016.
