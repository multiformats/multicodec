# multicodec-packed

[![](https://img.shields.io/badge/made%20by-Protocol%20Labs-blue.svg?style=flat-square)](http://ipn.io)
[![](https://img.shields.io/badge/project-multiformats-blue.svg?style=flat-square)](http://github.com/multiformats/multiformats)
[![](https://img.shields.io/badge/freenode-%23ipfs-blue.svg?style=flat-square)](http://webchat.freenode.net/?channels=%23ipfs)

> compact self-describing codecs

## Table of Contents

- [Motivation](#motivation)
- [How does it work? - Protocol Description](#how-does-it-work---protocol-description)
- [Multicodec-Packed Protocol Tables](#multicodec-packed-protocol-tables)
  - [Standard mcp protocol table](#standard-mcp-protocol-table)
- [Implementations](#implementations)
- [FAQ](#faq)
- [Maintainers](#maintainers)
- [Contribute](#contribute)
- [License](#license)

## Motivation

[Multicodecs](./README.md) are self-describing protocol/encoding streams. Multicodec-packed is a different representation of multicodec, which uses an agreed-upon "protocol path table". It is designed for use in short strings, such as keys or identifiers (such as [CID](https://github.com/ipld/cid)).

## How does it work? - Protocol Description

`multicodec-packed` is a _self-describing multiformat_, it wraps other formats with a tiny bit of self-description:

```sh
<mcp-code><encoded-data>
# or
<multicodec-packed-varint><encoded-data>
```

It can also be used as part of identifiers or keys to other data:

```
# suppose we have a value and a key to retrieve it
"<key>" -> <value>

# we can use multicodec-packed with the key to know what codec the value is in
"<mcp><key>" -> <value>
```

It is worth noting that multicodec-packed works very well in conjunction with [multihash](https://github.com/multiformats/multihash) and [multiaddr](https://github.com/multiformats/multiaddr), as you can prefix those values with a multicodec-packed to tell what they are.

## Multicodec-Packed Protocol Tables

Multicodec-packed uses "protocol tables" to agree upon the mapping from one multicodec-packed code (a single varint). These tables map an `<mcp-code>` to a full [multicodec protocol path](./README.md#the-protocol-path). These tables can be application specific, though -- like [with](https://github.com/multiformats/multihash) [other](https://github.com/multiformats/multibase) [multiformats](https://github.com/multiformats/multiaddr) -- we will keep a globally agreed upon table with common protocols and formats.

### Standard mcp protocol table

This is the standard multicodec-packed protocol table.

#### WARNING: WIP. this table is not ready for wide use.

TODO: see if IANA has a ready-made table for us to use here. Even just a listing of the most popular formats would be good enough.

```sh
code  codec
0x00  raw binary data
0x40  multicodec
0x41  multihash
0x42  multiaddr
# add the most popular serialization formats (asn.1, json, yml, xml, ...)
# add cbor, ion (ipld)
# add git, hg, and other VCSes
# add bitcoin, ethereum, and other blockchains
```

## Implementations

- None yet.
- [Add yours today!](https://github.com/multiformats/multicodec/edit/master/multicodec-packed.md)

## FAQ

> **Q. I have questions on multicodec, not listed here.**

That's not a question. But, have you checked the proper [multicodec FAQ](./README.md#faq)? Maybe your question is answered there. This FAQ is only specifically for multicodec-packed.

> **Q. Why?**

Because [multicodec](./README.md) is too long for identifiers. We needed something shorter.

> Why varints?

So that we have no limitation on protocols. Implementation note: you do not need to implement varints until the standard multicodec table has more than 127 functions.

> What kind of varints?

An Most Significant Bit unsigned varint, as defined by the [multiformats/unsigned-varint](https://github.com/multiformats/unsigned-varint).

> Don't we have to agree on a table of protocols?

Yes, but we already have to agree on what protocols themselves are, so this is not so hard. The table even leaves some room for custom protocol paths, or you can use your own tables. The standard table is only for common things.


## Maintainers

Captain: [@jbenet](https://github.com/jbenet).

## Contribute

Contributions welcome. Please check out [the issues](https://github.com/multiformats/multicodec/issues).

Check out our [contributing document](https://github.com/multiformats/multiformats/blob/master/contributing.md) for more information on how we work, and about contributing in general. Please be aware that all interactions related to multiformats are subject to the IPFS [Code of Conduct](https://github.com/ipfs/community/blob/master/code-of-conduct.md).

## License

[MIT](LICENSE) © Protocol Labs, Inc
