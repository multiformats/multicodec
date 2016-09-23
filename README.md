# multicodec

[![](https://img.shields.io/badge/made%20by-Protocol%20Labs-blue.svg?style=flat-square)](http://ipn.io)
[![](https://img.shields.io/badge/project-multiformats-blue.svg?style=flat-square)](http://github.com/multiformats/multiformats)
[![](https://img.shields.io/badge/freenode-%23ipfs-blue.svg?style=flat-square)](http://webchat.freenode.net/?channels=%23ipfs)

> self-describing codecs

## Table of Contents

- [Motivation](#motivation)
- [How does it work? - Protocol Description](#how-does-it-work---protocol-description)
- [Prefix examples](#prefix-examples)
- [prefix - codec - desc](#prefix---codec---desc)
- [The protocol path](#the-protocol-path)
- [Implementations](#implementations)
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
<multicodec-header><encoded-data>
# or
<varint-len><code>\n<encoded-data>
```

For example, let's encode a json doc:

```node
> // encode some json
> var str = JSON.stringify({"hello":"world"})
> var buf = multicodec.encode('json', str) // prepends multistream.header('/json')
> buf
<Buffer 06 2f 6a 73 6f 6e 2f 7b 22 68 65 6c 6c 6f 22 3a 22 77 6f 72 6c 64 22 7d>
> buf.toString('hex')
062f6a736f6e2f7b2268656c6c6f223a22776f726c64227d
> // decode, and find out what is in buf
> multicodec.decode(buf)
{ "codec": "json", "data": '{"hello": "world"}' }
```

So, `buf` is:

```
hex:   062f6a736f6e2f7b2268656c6c6f223a22776f726c64227d
ascii: json/\n{"hello":"world"}
```

The more you know! Let's try it again, this time with protobuf:

```
cat proto.c
```

See also: [multicodec-packed](./multicodec-packed.md).

## Prefix examples


```
prefix - codec - desc
----------------------------
// the bases
0x052f62696e2f - /bin/ - raw binary
0x042f62322f   - /b2/  - ascii base2 (binary)
0x052f6231362f - /b16/ - ascii base16 (hex)
0x052f6233322f - /b32/ - ascii base32
0x052f6235382f - /b58/ - ascii base58
0x052f6236342f - /b64/ - ascii base64

// unicode text
0xefbbbf - /utf8/ - UTF-8 encoded text

// the JSONs
062f6a736f6e2f      - /json/
062f63626f722f      - /cbor/
062f62736f6e2f      - /bson/
072f626a736f6e2f    - /bjson/
082f75626a736f6e2f  - /ubjson/

// protobuf
0a2f70726f746f6275662f - /protobuf/ - Protocol Buffers
072f6361706e702f       - /capnp/    - Cap-n-Proto
092f666c61746275662f   - /flatbuf/  - FlatBuffers

// archives
0x052f7461722f /tar/
0x052f7a69702f /zip/

// images
0x052f706e672f - /png/
```

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
/http/w3id.org/ipfs/ipfs-1.1.0.json
```

These path names happen to be resolvable -- not just in a "multicodec muxer(e.g [multistream]())" but -- in the internet as a whole (provided the program (or OS) knows how to use the `/ipfs` and `/http` protocols).

## Implementations

- [go-multicodec](https://github.com/jbenet/go-multicodec)
- [go-multistream](https://github.com/whyrusleeping/go-multistream) - Implements multistream, which uses multicodec for stream negotiation
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
