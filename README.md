# multicodec

[![](https://img.shields.io/badge/made%20by-Protocol%20Labs-blue.svg?style=flat-square)](http://ipn.io)
[![](https://img.shields.io/badge/project-multiformats-blue.svg?style=flat-square)](https://github.com/multiformats/multiformats)
[![](https://img.shields.io/badge/freenode-%23ipfs-blue.svg?style=flat-square)](https://webchat.freenode.net/?channels=%23ipfs)
[![](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

> Canonical table of of codecs used by various multiformats

## Table of Contents

- [Motivation](#motivation)
- [Description](#description)
- [Examples](#examples)
- [Multicodec table](#multicodec-table)
  - [Adding new multicodecs to the table](#adding-new-multicodecs-to-the-table)
- [Implementations](#implementations)
- [FAQ](#faq)
- [Contribute](#contribute)
- [License](#license)

## Motivation

Multicodec is an agreed-upon codec table. It is designed for use in binary representations, such as keys or identifiers (i.e [CID](https://github.com/ipld/cid)).

## Description

The code of a multicodec is usually encoded as unsigned varint as defined by [multiformats/unsigned-varint](https://github.com/multiformats/unsigned-varint). It is then used as a prefix to identify the data that follows.

## Examples

Multicodec is used in various [Multiformats](https://github.com/multiformats/multiformats). In [Multihash](https://github.com/multiformats/multihash) it is used to identify the hashes, in the machine-readable [Multiaddr](https://github.com/multiformats/multiaddr) to identify components such as IP addresses, domain names, identities, etc.

## Multicodec table

Find the canonical table of multicodecs at [table.csv](/table.csv). There's also a sortable [viewer](https://ipfs.io/ipfs/QmXec1jjwzxWJoNbxQF5KffL8q6hFXm9QwUGaa3wKGk6dT/#title=Multicodecs&src=https://raw.githubusercontent.com/multiformats/multicodec/master/table.csv).

### Adding new multicodecs to the table

The process to add a new multicodec to the table is the following:

- 1. Fork this repo
- 2. Update the table with the value you want to add
- 3. Submit a Pull Request

This ["first come, first assign"](https://github.com/multiformats/multicodec/pull/16#issuecomment-260146609) policy is a way to assign codes as they are most needed, without increasing the size of the table (and therefore the size of the multicodecs) too rapidly.

The first 127 bits are encoded as a single-byte varint, hence they are reserved for the most widely used multicodecs. So if you are adding your own codec to the table, you most likely would want to ask for a codec bigger than `0x80`.

## Implementations

- [go](https://github.com/multiformats/go-multicodec/)
- [JavaScript](https://github.com/multiformats/js-multicodec)
- [Python](https://github.com/multiformats/py-multicodec)
- [Haskell](https://github.com/multiformats/haskell-multicodec)
- [Elixir](https://github.com/nocursor/ex-multicodec)
- [Scala](https://github.com/fluency03/scala-multicodec)
- [Ruby](https://github.com/sleeplessbyte/ruby-multicodec)
- [Add yours today!](https://github.com/multiformats/multicodec/edit/master/table.csv)

### Code Ranges

There are some reserved code ranges.

#### MIME Types

The range 0x200000 - 0x2fffff is reserved for MIME types. Specifically, we've
reserved:

```
Range 0x200000 - 0x20ffff: reserved for 'application/*' (there currently are ~1,300 subtypes)
Range 0x210000 - 0x21ffff: reserved for 'audio/*' (there currently are ~150 subtypes)
Range 0x220000 - 0x22ffff: reserved for 'font/*' (there currently are ~8 subtypes)
Range 0x230000 - 0x23ffff: reserved for 'image/*' (there currently are ~60 subtypes)
Range 0x240000 - 0x24ffff: reserved for 'message/*' (there currently are ~18 subtypes)
Range 0x250000 - 0x25ffff: reserved for 'model/*' (there currently are ~24 subtypes)
Range 0x260000 - 0x26ffff: reserved for 'multipart/*' (there currently are ~13 subtypes)
Range 0x270000 - 0x27ffff: reserved for 'text/*' (there currently are ~71 subtypes)
Range 0x280000 - 0x28ffff: reserved for 'video/*' (there currently are ~78 subtypes)
```

Everything from 0x290000 to 0x2fffff is reserved for future media types.

## FAQ

> Why varints?

So that we have no limitation on protocols.

> What kind of varints?

An Most Significant Bit unsigned varint, as defined by the [multiformats/unsigned-varint](https://github.com/multiformats/unsigned-varint).

> Don't we have to agree on a table of protocols?

Yes, but we already have to agree on what protocols themselves are, so this is not so hard. The table even leaves some room for custom protocol paths, or you can use your own tables. The standard table is only for common things.

> Where did multibase go?

For a period of time, the [multibase](https://github.com/multiformats/multibase) prefixes lived in this table. However, multibase prefixes are *symbols* that may map to *multiple* underlying byte representations (that may overlap with byte sequences used for other multicodecs). Including them in a table for binary/byte identifiers lead to more confusion than it solved.

You can still find the table in [multibase.csv](https://github.com/multiformats/multibase/blob/master/multibase.csv).

> Can I use multicodec for my own purpose?

Sure, you can use multicodec whenever you have the need for self-identifiable data. Just prefix your own data with the corresponding varint encodec multicodec.

## Contribute

Contributions welcome. Please check out [the issues](https://github.com/multiformats/multicodec/issues).

Check out our [contributing document](https://github.com/multiformats/multiformats/blob/master/contributing.md) for more information on how we work, and about contributing in general. Please be aware that all interactions related to multiformats are subject to the IPFS [Code of Conduct](https://github.com/ipfs/community/blob/master/code-of-conduct.md).

Small note: If editing the README, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

## License

This repository is only for documents. All of these are licensed under the [CC-BY-SA 3.0](https://ipfs.io/ipfs/QmVreNvKsQmQZ83T86cWSjPu2vR3yZHGPm5jnxFuunEB9u) license © 2016 Protocol Labs Inc. Any code is under a [MIT](LICENSE) © 2016 Protocol Labs Inc.
