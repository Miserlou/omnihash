# omnihash

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

MIT license.