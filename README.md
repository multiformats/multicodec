# multicodec

[![](https://img.shields.io/badge/made%20by-Protocol%20Labs-blue.svg?style=flat-square)](http://ipn.io)
[![](https://img.shields.io/badge/project-multiformats-blue.svg?style=flat-square)](https://github.com/multiformats/multiformats)
[![](https://img.shields.io/badge/freenode-%23ipfs-blue.svg?style=flat-square)](https://webchat.freenode.net/?channels=%23ipfs)
[![](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

> Compact self-describing codecs. Save space by using predefined multicodec tables.

## Table of Contents

- [Motivation](#motivation)
- [How does it work? - Protocol Description](#how-does-it-work---protocol-description)
- [Multicodec table](#multicodec-table)
- [Implementations](#implementations)
- [FAQ](#faq)
- [Maintainers](#maintainers)
- [Contribute](#contribute)
- [License](#license)

## Motivation

[Multistreams](https://github.com/multiformats/multistream) are self-describing protocol/encoding streams. Multicodec uses an agreed-upon "protocol table". It is designed for use in short strings, such as keys or identifiers (i.e [CID](https://github.com/ipld/cid)).

## Protocol Description - How does the protocol work?

`multicodec` is a _self-describing multiformat_, it wraps other formats with a tiny bit of self-description. A multicodec identifier may either be a varint (in a byte string) or a symbol (in a text string).

A chunk of data identified by multicodec will look like this:

```sh
<multicodec><encoded-data>
# To reduce the cognitive load, we sometimes might write the same line as:
<mc><data>
```

Another useful scenario is when using the multicodec as part of the keys to access data, example:

```
# suppose we have a value and a key to retrieve it
"<key>" -> <value>

# we can use multicodec with the key to know what codec the value is in
"<mc><key>" -> <value>
```

It is worth noting that multicodec works very well in conjunction with [multihash](https://github.com/multiformats/multihash) and [multiaddr](https://github.com/multiformats/multiaddr), as you can prefix those values with a multicodec to tell what they are.

## MulticodecProtocol Tables

Multicodec uses "protocol tables" to agree upon the mapping from one multicodec code. These tables can be application specific, though -- like [with](https://github.com/multiformats/multihash) [other](https://github.com/multiformats/multibase) [multiformats](https://github.com/multiformats/multiaddr) -- we will keep a globally agreed upon table with common protocols and formats.

## Multicodec table

The full table can be found at [table.csv](/table.csv) inside this repo. Codes
prefixed with `0x` are varint multicodecs and all others are symbolic.

### Adding new multicodecs to the table

The process to add a new multicodec to the table is the following:

- 1. Fork this repo
- 2. Update the table with the value you want to add
- 3. Submit a Pull Request

This ["first come, first assign"](https://github.com/multiformats/multicodec/pull/16#issuecomment-260146609) policy is a way to assign codes as they are most needed, without increasing the size of the table (and therefore the size of the multicodecs) too rapidly.

## Implementations

- [go](https://github.com/multiformats/go-multicodec/)
- [JavaScript](https://github.com/multiformats/js-multicodec)
- [Python](https://github.com/multiformats/py-multicodec)
- [Haskell](https://github.com/multiformats/haskell-multicodec)
- [Add yours today!](https://github.com/multiformats/multicodec/edit/master/table.csv)

## Multicodec Path, also known as [`multistream`](https://github.com/multiformats/multistream)

Multicodec defines a table for the most common data serialization formats that can be expanded overtime or per application bases, however, in order for two programs to talk with each other, they need to know before hand which table or table extension is being used.

In order to enable self descriptive data formats or streams that can be dynamically described, without the formal set of adding a binary packed code to a table, we have [`multistream`](https://github.com/multiformats/multistream), so that applications can adopt multiple data formats for their streams and with that create different protocols.

## FAQ

> **Q. I have questions on multicodec, not listed here.**

That's not a question. But, have you checked the proper [multicodec FAQ](./README.md#faq)? Maybe your question is answered there. This FAQ is only specifically for multicodec.

> **Q. Why?**

Because [multistream](https://github.com/multiformats/multistream) is too long for identifiers. We needed something shorter.

> **Q. Why varints?**

So that we have no limitation on protocols. Implementation note: you do not need to implement varints until the standard multicodec table has more than 127 functions.

> **Q. What kind of varints?**

An Most Significant Bit unsigned varint, as defined by the [multiformats/unsigned-varint](https://github.com/multiformats/unsigned-varint).

> **Q. Don't we have to agree on a table of protocols?**

Yes, but we already have to agree on what protocols themselves are, so this is not so hard. The table even leaves some room for custom protocol paths, or you can use your own tables. The standard table is only for common things.

> **Q. Why distinguish between bytes and text?**

For completeness, we consider
[multibase](https://github.com/multiformats/multibase) prefixes to be
multicodecs. However multibase prefixes occur in *text*, and are therefore *symbols*. They may (or may not) have some underlying binary representation but that changes based on the text encoding used.

## Maintainers

Captain: [@jbenet](https://github.com/jbenet).

## Contribute

Contributions welcome. Please check out [the issues](https://github.com/multiformats/multicodec/issues).

Check out our [contributing document](https://github.com/multiformats/multiformats/blob/master/contributing.md) for more information on how we work, and about contributing in general. Please be aware that all interactions related to multiformats are subject to the IPFS [Code of Conduct](https://github.com/ipfs/community/blob/master/code-of-conduct.md).

Small note: If editing the README, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

## License

This repository is only for documents. All of these are licensed under the [CC-BY-SA 3.0](https://ipfs.io/ipfs/QmVreNvKsQmQZ83T86cWSjPu2vR3yZHGPm5jnxFuunEB9u) license © 2016 Protocol Labs Inc. Any code is under a [MIT](LICENSE) © 2016 Protocol Labs Inc.
