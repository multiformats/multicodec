# multicodec

[![](https://img.shields.io/badge/made%20by-Protocol%20Labs-blue.svg?style=flat-square)](http://ipn.io)
[![](https://img.shields.io/badge/project-multiformats-blue.svg?style=flat-square)](http://github.com/multiformats/multiformats)
[![](https://img.shields.io/badge/freenode-%23ipfs-blue.svg?style=flat-square)](http://webchat.freenode.net/?channels=%23ipfs)

> Make data and streams self-described by prefixing them with human readable or binary packed codecs. `multicodec` offers a base table, but can also be extended with extra tables by application basis.

## Table of Contents

- [Motivation](#motivation)
  - [How does it work? - Protocol Description](#how-does-it-work---protocol-description)
  - [The protocol path](#the-protocol-path)
- [Multicodec table](#multicodec-table)
- [Implementations](#implementations)
  - [Implementation details]()
- [FAQ](#faq)
- [Maintainers](#maintainers)
- [Contribute](#contribute)
- [License](#license)

## Motivation

Multicodecs are self-describing protocol/encoding streams. (Note that a file is a stream). It's designed to address the perennial problem:

> I have a bitstring, what codec is the data coded with!?

Instead of arguing about which data serialization library is the best, let's just pick the simplest one now, and build _upgradability_ into the system. Choices are never _forever_. Eventually all systems are changed. So, embrace this fact of reality, and build change into your system now.

Multicodec frees you from the tyranny of past mistakes. Instead of trying to figure it all out beforehand, or continue using something that we can all agree no longer fits, why not allow the system to _evolve_ and _grow_ with the use cases of today, not yesterday.

To decode an incoming stream of data, a program must either (a) know the format of the data a priori, or (b) learn the format from the data itself. (a) precludes running protocols that may provide one of many kinds of formats without prior agreement on which. multistream makes (b) neat using self-description.

Moreover, this self-description allows straightforward layering of protocols without having to implement support in the parent (or encapsulating) one.

## How does it work? - Protocol Description

`multicodec` is a _self-describing multiformat_, it wraps other formats with a tiny bit of self-description:

```sh
<varint-len><multicodec>\n<encoded-data>
```

For example, let's encode a json doc:

```JavaScript
// encode some json
const buf = new Buffer(JSON.stringify({ hello: 'world' }))

const prefixedBuf = multicodec.addPrefix('json', str) // prepends multicodec ('json')
console.log(prefixedBuf)
// <Buffer 06 2f 6a 73 6f 6e 2f 7b 22 68 65 6c 6c 6f 22 3a 22 77 6f 72 6c 64 22 7d>

const.log(prefixedBuf.toString('hex'))
// 062f6a736f6e2f7b2268656c6c6f223a22776f726c64227d

// let's get the Multicodec, and get the data back

const codec = multicodec.getMulticodec(prefixedBuf)
console.log(codec)
// json

console.log(multicodec.rmPrefix(prefixedBuf).toString())
// "{ \"hello\": \"world\" }
```

So, `buf` is:

```
hex:   062f6a736f6e2f7b2268656c6c6f223a22776f726c64227d
ascii: /json/"{\"hello\":\"world\"}
```

Note that on the ascii version, the varint at the beginning is not being represented, you should account that.

For a binary packed version of the multicodecs, see [multicodec-packed](./multicodec-packed.md).

## The protocol path

`multicodec` allows us to specify different protocols in a universal namespace, that way being able to recognize, multiplex, and embed them easily. We use the notion of a `path` instead of an `id` because it is meant to be a Unix-friendly URI.

A good path name should be decipherable -- meaning that if some machine or developer -- who has no idea about your protocol -- encounters the path string, they should be able to look it up and resolve how to use it.

An example of a good path name is:

```
/bittorrent.org/1.0
```

An example of a _great_ path name is:

```
/ipfs/Qmaa4Rw81a3a1VEx4LxB7HADUAXvZFhCoRdBzsMZyZmqHD/ipfs.protocol
/http/w3id.org/ipfs/1.1.0
```

These path names happen to be resolvable -- not just in a "multicodec muxer(e.g [multistream](https://github.com/multiformats/multistream))" but -- in the internet as a whole (provided the program (or OS) knows how to use the `/ipfs` and `/http` protocols).

## Multicodec table

| prefix                        | codec           | description             | [packed][p] | multibase only |
|-------------------------------|-----------------|-------------------------|-------------|----------------|
| **Miscelaneous**                                                                                         |
| 0x052f62696e2f                | /bin/           | raw binary              | 0x00        | n/a            |
| **Bases encodings**                                                                                      |
|                               | /base1/         | unary                   |             | 1              |
|                               | /base2/         | binary (0 and 1)        |             | 0              |
|                               | /base8/         | octal                   |             | 7              |
|                               | /base10/        | decimal                 |             | 9              |
|                               | /base16/        | hexadecimal             |             | F, f           |
|                               | /base32/        | rfc4648                 |             | U, u           |
|                               | /base32hex/     | rfc4648                 |             | V, v           |
|                               | /base58flickr/  | base58 flicker          |             | Z              |
|                               | /base58btc/     | base58 bitcoin          |             | z              |
|                               | /base64/        | rfc4648                 |             | y              |
|                               | /base64url/     | rfc4648                 |             | Y              |
| **Serialization formats**                                                                                |
| 0x062f6a736f6e2f              | /json/          |                         |             | n/a            |
| 0x062f63626f722f              | /cbor/          |                         |             | n/a            |
| 0x062f62736f6e2f              | /bson/          |                         |             | n/a            |
| 0x072f626a736f6e2f            | /bjson/         |                         |             | n/a            |
| 0x082f75626a736f6e2f          | /ubjson/        |                         |             | n/a            |
| 0x0a2f70726f746f6275662f      | /protobuf/      | Protocol Buffers        |             | n/a            |
| 0x072f6361706e702f            | /capnp/         | Cap-n-Proto             |             | n/a            |
| 0x092f666c61746275662f        | /flatbuf/       | FlatBuffers             |             | n/a            |
| 0x052f726c702f                | /rlp/           | recursive length prefix | 0x60        | n/a            |
| **Multiformats**                                                                                         |
| 0x182f6d756c7469636f6465632f  | /multicodec/    |                         | 0x30        | n/a            |
| 0x162f6d756c7469686173682f    | /multihash/     |                         | 0x31        | n/a            |
| 0x162f6d756c7469616464722f    | /multiaddr/     |                         | 0x32        | n/a            |
| **Multihashes**                                                                                          |
|                               | /sha1/          |                         | 0x11        | n/a            |
|                               | /sha2-256/      |                         | 0x12        | n/a            |
|                               | /sha2-512/      |                         | 0x13        | n/a            |
|                               | /sha3-256/      |                         | 0x16        | n/a            |
|                               | /sha3-384/      |                         | 0x15        | n/a            |
|                               | /sha3-512/      |                         | 0x14        | n/a            |
|                               | /shake-128/     |                         | 0x18        | n/a            |
|                               | /shake-256/     |                         | 0x19        | n/a            |
|                               | /blake2b/       |                         | 0x40        | n/a            |
|                               | /blake2s/       |                         | 0x41        | n/a            |
| **Multiaddrs**                                                                                           |
|                               | /ip4/           |                         | 0x04        | n/a            |
|                               | /ip6/           |                         | 0x29        | n/a            |
|                               | /tcp/           |                         | 0x06        | n/a            |
|                               | /udp/           |                         | 0x11        | n/a            |
|                               | /dccp/          |                         | 0x21        | n/a            |
|                               | /sctp/          |                         | 0x84        | n/a            |
|                               | /udt/           |                         | 0x012D      | n/a            |
|                               | /utp/           |                         | 0x012E      | n/a            |
|                               | /ipfs/          |                         | 0x2A        | n/a            |
|                               | /http/          |                         | 0x01E0      | n/a            |
|                               | /https/         |                         | 0x01BB      | n/a            |
|                               | /ws/            |                         | 0x01DD      | n/a            |
|                               | /onion/         |                         | 0x01BC      | n/a            |
| **Archiving formats**                                                                                    |
| 0x052f7461722f                | /tar/           |                         |             | n/a            |
| 0x052f7a69702f                | /zip/           |                         |             | n/a            |
| **Image formats**                                                                                        |
| 0x052f706e672f                | /png/           |                         |             | n/a            |
|                               | /jpg/           |                         |             | n/a            |
| **Video formats**                                                                                        |
|                               | /mp4/           |                         |             | n/a            |
|                               | /mkv/           |                         |             | n/a            |
| **Blockchain formats**                                                                                   |
|                               |                 |                         |             | n/a            |
| **VCS formats**                                                                                          |
|                               |                 |                         |             | n/a            |
| **IPLD formats**                                                                                         |
|                               | /dag-pb/        | MerkleDAG protobuf      |             | n/a            |
|                               | /dag-cbor/      | MerkleDAG cbor          |             | n/a            |
|                               | /eth-rlp/       | Ethereum Block RLP      |             | n/a            |

Note: Base encodings present a multibase encoding special char, so that the codec doesn't break the encoded version of the data it is describing.

## Implementations

- multicodec
  - [go-multicodec](https://github.com/multiformats/go-multicodec)
- multicodec-packed
  - [go-multicodec-packed](https://github.com/multiformats/go-multicodec-packed)
  - [js-multicodec-packed](https://github.com/multiformats/js-multicodec-packed)
- multistream
  - [go-multistream](https://github.com/multiformats/go-multistream) - Implements multistream, which uses multicodec for stream negotiation
  - [js-multistream](https://github.com/multiformats/js-multistream) - Implements multistream, which uses multicodec for stream negotiation
  - [clj-multicodec](https://github.com/greglook/clj-multicodec)

## FAQ

> **Q. Why?**

Today, people speak many languages, and use common ones to interface. But every "common language" has evolved over time, or even fundamentally switched. Why should we expect programs to be any different?

And the reality is they're not. Programs use a variety of encodings. Today we like JSON. Yesterday, XML was all the rage. XDR solved everything, but it's kinda retro. Protobuf is still too cool for school. capnp ("cap and proto") is
for cerealization hipsters.

The one problem is figuring out what we're speaking. Humans are pretty smart, we pick up all sorts of languages over time. And we can always resort to pointing and grunting (the ascii of humanity).

Programs have a harder time. You can't keep piping json into a protobuf decoder and hope they align. So we have to help them out a bit. That's what multicodec is for.

> **Q. Why "codec" and not "encoder" and "decoder"?**

Because they're the same thing. Which one of these is the encoder and which the decoder?

    5555 ----[ THING ]---> 8888
    5555 <---[ THING ]---- 8888

> **Q. Full paths are too big for my use case, is there something smaller?**

Yes, check out [multicodec-packed](./multicodec-packed.md). It uses a varint and a table to achieve the same thing.

## Maintainers

Captain: [@jbenet](https://github.com/jbenet).

## Contribute

Contributions welcome. Please check out [the issues](https://github.com/multiformats/multicodec/issues).

Check out our [contributing document](https://github.com/multiformats/multiformats/blob/master/contributing.md) for more information on how we work, and about contributing in general. Please be aware that all interactions related to multiformats are subject to the IPFS [Code of Conduct](https://github.com/ipfs/community/blob/master/code-of-conduct.md).

## License

[MIT](LICENSE)

[p](https://github.com/multiformats/multicodec/blob/master/multicodec-packed.md)
