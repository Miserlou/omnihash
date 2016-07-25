# omnihash [![Build Status](https://travis-ci.org/Miserlou/omnihash.svg)](https://travis-ci.org/Miserlou/omnihash) [![PyPI](https://img.shields.io/pypi/v/omnihash.svg)](https://pypi.python.org/pypi/omnihash)

Tiny little tool to hash strings and files using various common hashing algorithms.

## Installation

    pip install omnihash

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
    Hashing file /etc/hosts..
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

You can also pass multiple inputs and force string-hashing with `-s`.

MIT license, 2016.
