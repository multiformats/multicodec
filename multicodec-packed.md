# multicodec-packed

[![](https://img.shields.io/badge/made%20by-Protocol%20Labs-blue.svg?style=flat-square)](http://ipn.io)
[![](https://img.shields.io/badge/project-multiformats-blue.svg?style=flat-square)](http://github.com/multiformats/multiformats)
[![](https://img.shields.io/badge/freenode-%23ipfs-blue.svg?style=flat-square)](http://webchat.freenode.net/?channels=%23ipfs)

> compact self-describing codecs. Save space by using predefined multicodec tables.

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

[Multicodecs](./README.md) are self-describing protocol/encoding streams. Multicodec-packed is a different representation of multicodec, which uses an agreed-upon "protocol table". It is designed for use in short strings, such as keys or identifiers (i.e [CID](https://github.com/ipld/cid)).

## Protocol Description - How does the protocol work?

`multicodec-packed` is a _self-describing multiformat_, it wraps other formats with a tiny bit of self-description. A multicodec-packed identifier is both a varint and the code identifying the following data, this means that the most significant bit of every multicodec-packed code is reserved to signal the continuation.

This way, a chunk of data identified by multicodec will look like this:

```sh
<multicodec-packed-varint><encoded-data>
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

Multicodec-packed uses "protocol tables" to agree upon the mapping from one multicodec-packed code (a single varint). These tables map an `<mcp-code>` to a full [multicodec protocol path](./README.md#the-protocol-path). These tables can be application specific, though -- like [with](https://github.com/multiformats/multihash) [other](https://github.com/multiformats/multibase) [multiformats](https://github.com/multiformats/multiaddr) -- we will keep a globally agreed upon table with common protocols and formats.

## Implementations

- [go](https://github.com/multiformats/go-multicodec-packed/)
- [JavaScript](https://github.com/multiformats/js-multicodec-packed)
- [Add yours today!](https://github.com/multiformats/multicodec/edit/master/multicodec-packed.md)

## FAQ

> **Q. I have questions on multicodec, not listed here.**

That's not a question. But, have you checked the proper [multicodec FAQ](./README.md#faq)? Maybe your question is answered there. This FAQ is only specifically for multicodec-packed.

> **Q. Why?**

Because [multicodec](./README.md) is too long for identifiers. We needed something shorter.

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
