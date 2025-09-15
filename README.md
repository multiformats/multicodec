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
- [Reserved Code Ranges](#reserved-code-ranges)
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

Find the canonical table of multicodecs at [table.csv](/table.csv).

### Status

Each multicodec is marked with a status:

* draft - this codec has been reserved but may be reassigned if it doesn't gain wide adoption.
* permanent - this codec has been widely adopted and may not reassigned.
* deprecated - this codec has been deprecated.

NOTE: Just because a codec is marked draft, don't assume that it can be re-assigned. Check to see if it ever gained wide adoption and, if so, mark it as permanent.

### Tag Categories

Each multicodec entry in the table.csv has a "tag" column that helps categorize the entry type. When adding a new multicodec, it's important to assign the correct tag. Here are descriptions of the most common tags:

* **multihash**: Entries for cryptographic hash functions as described in [multihash](https://github.com/multiformats/multihash). Multihash is a protocol for differentiating outputs from various well-established cryptographic hash functions, addressing size and encoding considerations.

* **hash**: Non-cryptographic hash functions, which are not suitable for content addressing systems but may have other uses. As noted in the [multihash documentation](https://github.com/multiformats/multihash#non-cryptographic-hash-functions), these have specialized use-cases where identifying non-cryptographic hash functions by multihash may be desirable.

* **key**: Cryptographic key types, including public and private keys for various cryptographic algorithms.

* **multiaddr**: Network address formats as defined in [multiaddr](https://github.com/multiformats/multiaddr). Multiaddr aims to make network addresses future-proof, composable, and efficient.

* **ipld**: [InterPlanetary Linked Data](https://ipld.io/) formats. These codecs are suitable for use as a codec in a [CID](https://github.com/multiformats/cid) and will deserialize linked data that may contain links to other data.

* **serialization**: Similar to "ipld" but does not materialize links. For example, JSON and CBOR have the "serialization" tag, while DAG-JSON and DAG-CBOR have the "ipld" tag because they handle links.

* **varsig**: Signature formats as described in [varsig](https://github.com/ChainAgnostic/varsig). Varsig is a multiformat for describing signatures over IPLD data and raw bytes in a way that preserves information about the payload and canonicalization information.

* **namespace**: Namespace identifiers for various protocols and systems.

Selecting the appropriate tag helps maintain organization in the table and provides context for how a codec is expected to be used.

### Adding new multicodecs to the table

The process to add a new multicodec to the table is the following:

1. Fork this repo
2. Add your codecs to the table. Each newly proposed codec must have:
  1. A unique codec.
  2. A unique name.
  3. A category.
  4. A status of "draft".
3. Submit a Pull Request

This ["first come, first assign"](https://github.com/multiformats/multicodec/pull/16#issuecomment-260146609) policy is a way to assign codes as they are most needed, without increasing the size of the table (and therefore the size of the multicodecs) too rapidly.

The first 127 values are encoded as a single-byte varint, hence they are reserved for the most widely used multicodecs. So if you are adding your own codec to the table, you most likely would want to ask for a codec bigger than `0x80`.

Codec names should be easily convertible to constants in common programming languages using basic transformation rules (e.g. upper-case, conversion of `-` to `_`, etc.). Therefore they should contain alphanumeric characters, with the first character being alphabetic. The primary delimiter for multi-part names should be `-`, with `_` reserved for cases where a secondary delimiter is required. For example: `bls12_381-g1-pub` contains 3 parts: `bls12_381`, `g1` and `pub`, where `bls12_381` is "BLS12 381" which is not commonly written as "BLS12381" and therefore requires a secondary separator.

The `validate.py` script can be used to validate the table once it's edited.

## Implementations

- [go](https://github.com/multiformats/go-multicodec/)
- [JavaScript](https://github.com/multiformats/js-multicodec)
- Python
  - [py-multicodec](https://github.com/multiformats/py-multicodec)
  - `multicodec` sub-module of Python module [multiformats](https://github.com/hashberg-io/multiformats)
- [Haskell](https://github.com/multiformats/haskell-multicodec)
- [Elixir](https://github.com/nocursor/ex-multicodec)
- [Scala](https://github.com/fluency03/scala-multicodec)
- [Ruby](https://github.com/sleeplessbyte/ruby-multicodec)
- Java
  - [java-multicodec](https://github.com/richardbergquist/java-multicodec)
  - [copper-multicodec](https://github.com/filip26/copper-multicodec)
- Kotlin
  - `multicodec` part of Kotlin project [multiformat](https://github.com/erwin-kok/multiformat)
- Zig
  - `multicodec` part of Zig project [multiformats-zig](https://github.com/zen-eth/multiformats-zig)
- Swift
  - `Multicodec` part of [MultiformatsKit](https://github.com/ATProtoKit/MultiformatsKit)
- [Add yours today!](https://github.com/multiformats/multicodec/edit/master/table.csv)

## Reserved Code Ranges

The following code ranges have special meaning and may only have meanings assigned to as specified in their description:

### Private Use Area

*Range*: `0x300000 – 0x3FFFFF`

Codes in this range are reserved for internal use by applications and will never be assigned any meaning as part of the Multicodec specification.

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

Sure, you can use multicodec whenever you have the need for self-identifiable data. Just prefix your own data with the corresponding varint encoded multicodec.

## Contribute

Contributions welcome. Please check out [the issues](https://github.com/multiformats/multicodec/issues).

Check out our [contributing document](https://github.com/multiformats/multiformats/blob/master/contributing.md) for more information on how we work, and about contributing in general. Please be aware that all interactions related to multiformats are subject to the IPFS [Code of Conduct](https://github.com/ipfs/community/blob/master/code-of-conduct.md).

Small note: If editing the README, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

## License

This repository is only for documents. All of these are licensed under the [CC-BY-SA 3.0](https://ipfs.io/ipfs/QmVreNvKsQmQZ83T86cWSjPu2vR3yZHGPm5jnxFuunEB9u) license © 2016 Protocol Labs Inc. Any code is under a [MIT](LICENSE) © 2016 Protocol Labs Inc.
