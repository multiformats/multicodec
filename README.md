# multicodec

[![](https://img.shields.io/badge/made%20by-Protocol%20Labs-blue.svg?style=flat-square)](http://ipn.io)
[![](https://img.shields.io/badge/project-multiformats-blue.svg?style=flat-square)](http://github.com/multiformats/multiformats)
[![](https://img.shields.io/badge/freenode-%23ipfs-blue.svg?style=flat-square)](http://webchat.freenode.net/?channels=%23ipfs)

> compact self-describing codecs. Save space by using predefined multicodec tables.

## Table of Contents

- [Motivation](#motivation)
- [How does it work? - Protocol Description](#how-does-it-work---protocol-description)
- [Multicodec tables](#multicodec-tables)
  - [Standard multicodec table](#standard-mcp-protocol-table)
- [Implementations](#implementations)
- [FAQ](#faq)
- [Maintainers](#maintainers)
- [Contribute](#contribute)
- [License](#license)

## Motivation

[Multistreams](https://github.com/multiformats/multistream) are self-describing protocol/encoding streams. Multicodec uses an agreed-upon "protocol table". It is designed for use in short strings, such as keys or identifiers (i.e [CID](https://github.com/ipld/cid)).

## Protocol Description - How does the protocol work?

`multicodec` is a _self-describing multiformat_, it wraps other formats with a tiny bit of self-description. A multicodec identifier is both a varint and the code identifying the following data, this means that the most significant bit of every multicodec code is reserved to signal the continuation.

This way, a chunk of data identified by multicodec will look like this:

```sh
<multicodec-varint><encoded-data>
# To reduce the cognitive load, we sometimes might write the same line as:
<mcp><data>
```

Another useful scenario is when using the multicodec-packed as part of the keys to access data, example:

```
# suppose we have a value and a key to retrieve it
"<key>" -> <value>

# we can use multicodec-packed with the key to know what codec the value is in
"<mcp><key>" -> <value>
```

It is worth noting that multicodec-packed works very well in conjunction with [multihash](https://github.com/multiformats/multihash) and [multiaddr](https://github.com/multiformats/multiaddr), as you can prefix those values with a multicodec-packed to tell what they are.

## Multicodec-Packed Protocol Tables

Multicodecuses "protocol tables" to agree upon the mapping from one multicodec code (a single varint). These tables can be application specific, though -- like [with](https://github.com/multiformats/multihash) [other](https://github.com/multiformats/multibase) [multiformats](https://github.com/multiformats/multiaddr) -- we will keep a globally agreed upon table with common protocols and formats.

## Multicodec table

```csv
codec,              description,              code

miscelaneous
bin,                raw binary,               0x55

bases encodings
base1,              unary,                    0x01
base2,              binary (0 and 1),         0x00
base8,              octal,                    0x07
base10,             decimal,                  0x09
base16,             hexadecimal,              0x
base32,             rfc4648,                  0x
base32hex,          rfc4648,                  0x
base58flickr,       base58 flicker,           0x
base58btc,          base58 bitcoin,           0x
base64,             rfc4648,                  0x
base64url,          rfc4648,                  0x

serialization formats
json,               ,                         0x
cbor,               ,                         0x
bson,               ,                         0x
bjson,              ,                         0x
ubjson,             ,                         0x
protobuf,           Protocol Buffers,         0x
capnp,              Cap-n-Proto,              0x
flatbuf,            FlatBuffers,              0x
rlp,                recursive length prefix,  0x60

multiformats
multicodec,         ,                         0x30
multihash,          ,                         0x31
multiaddr,          ,                         0x32
multibase,          ,                         0x33

multihashes
sha1,               ,                         0x11
sha2-256,           ,                         0x12
sha2-512,           ,                         0x13
sha3-224,           ,                         0x17
sha3-256,           ,                         0x16
sha3-384,           ,                         0x15
sha3-512,           ,                         0x14
shake-128,          ,                         0x18
shake-256,          ,                         0x19
murmur3             ,                         0x22
blake2b,            ,                         0x40
blake2s,            ,                         0x41
dbl-sha2-256        ,                         0x56
reserved for apps,  appl specific range,      0x4000-0x40f0

multiaddrs
ip4,                ,                         0x04
ip6,                ,                         0x29
tcp,                ,                         0x06
udp,                ,                         0x11
dccp,               ,                         0x21
sctp,               ,                         0x84
udt,                ,                         0x012D
utp,                ,                         0x012E
ipfs,               ,                         0x2A
http,               ,                         0x01E0
https,              ,                         0x01BB
ws,                 ,                         0x01DD
onion,              ,                         0x01BC

archiving formats
tar,                ,                         0x
zip,                ,                         0x

image formats
png,                ,                         0x
jpg,                ,                         0x

video formats
mp4,                ,                         0x
mkv,                ,                         0x

blockchain formats

VCS formats

IPLD formats
dag-pb,             MerkleDAG protobuf,       0x70
dag-cbor,           MerkleDAG cbor,           0x71
eth-block,          Ethereum Block (RLP),     0x90
eth-tx,             Ethereum Tx (RLP),        0x91
bitcoin-block,      Bitcoin Block,            0xb0
bitcoin-tx,         Bitcoin Tx,               0xb1
zcash-block,        Zcash Block,              0xc0
zcash-tx,           Zcash Tx,                 0xc1
stellar-block,      Stellar Block,            0xd0
stellar-tx,         Stellar Tx,               0xd1
```

## Implementations

- [go](https://github.com/multiformats/go-multicodec/)
- [JavaScript](https://github.com/multiformats/js-multicodec)
- [Add yours today!](https://github.com/multiformats/multicodec/edit/master/multicodec.md)

## FAQ

> **Q. I have questions on multicodec, not listed here.**

That's not a question. But, have you checked the proper [multicodec FAQ](./README.md#faq)? Maybe your question is answered there. This FAQ is only specifically for multicodec-packed.

> **Q. Why?**

Because [multistream](https://github.com/multiformats/multistream) is too long for identifiers. We needed something shorter.

> **Q. Why varints?**

So that we have no limitation on protocols. Implementation note: you do not need to implement varints until the standard multicodec table has more than 127 functions.

> **Q. What kind of varints?**

An Most Significant Bit unsigned varint, as defined by the [multiformats/unsigned-varint](https://github.com/multiformats/unsigned-varint).

> **Q. Don't we have to agree on a table of protocols?**

Yes, but we already have to agree on what protocols themselves are, so this is not so hard. The table even leaves some room for custom protocol paths, or you can use your own tables. The standard table is only for common things.

## Maintainers

Captain: [@jbenet](https://github.com/jbenet).

## Contribute

Contributions welcome. Please check out [the issues](https://github.com/multiformats/multicodec/issues).

Check out our [contributing document](https://github.com/multiformats/multiformats/blob/master/contributing.md) for more information on how we work, and about contributing in general. Please be aware that all interactions related to multiformats are subject to the IPFS [Code of Conduct](https://github.com/ipfs/community/blob/master/code-of-conduct.md).

## License

[MIT](LICENSE)
