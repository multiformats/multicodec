# multicodec - self-describing codings

multicodec is one of the self-describing multiformats. It's designed to address the perennial problem:

> I have a bitstring, what codec is the data coded with!?

Instead of arguing about which data serialization library is the best, let's just pick the simplest one now, and build _upgradability_ into the system. Choices are never _forever_. Eventually all systems are changed. So, embrace this fact of reality, and build change into your system now.

multicodec frees you from the tyranny of past mistakes. Someone wise said "every choice (in computing) is eventually incorrect". Instead of trying to figure it all out beforehand, or continue using something that we can all agree no longer fits, why not allow the system to _evolve_ and _grow_ with the use cases of today, not yesterday.

## How does it work?

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

# FAQ

> **Q. Why?**

Today, people speak many languages, and use common ones to interface. But every "common language" has evolved over time, or even fundamentally switched. Why should we expect programs to be any different?

And the reality is they're not. Programs use a variety of encodings. Today we like JSON. Yesterday, XML was all the rage. XDR solved everything, but it's kinda retro. Protobuf is still too cool for school. capnp ("cap and proto") is
for cerealization hipsters.

The one problem is figuring out what we're speaking. Humans are pretty smart, we pick up all sorts of languages over time. And we can always resort to pointing and grunting (the ascii of humanity).

Programs have a harder time. You can't keep piping json into a protobuf decoder and hope they align. So we have to help them out a bit. That's what multicodec is for.

> **Q. Why "codec" and not "encoder" and "decoder"?**

Because they're the same thing. Which one of these is the encoder and which the decoder?

    5555 ----[ THING ]---> 8888
    5555 <---[ THING ]---- 5555
