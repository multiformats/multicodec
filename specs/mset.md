# MSET is a "hashing" function that encode repating sets of bytes

The name is inspired by the memset function.

It is similar to identity as it isn't a hash, but a complete representation of the data.

The main goal of MSET is not to be used for effective data compression.
The goal is instead to compress the trivial cases of data padding.

## Digest decoding

```
<varuint count - 2><pattern>
```

First, you read a varuint, this is the number of time the pattern must be repeated minus two (so you add two to get the true value).

Everything left in your buffer is the pattern to repeat.

If there is nothing left in the buffer (that mean that the count is the ONLY thing in the digest), then the pattern is `0x00`.

The varuint count MUST be minimal and complete, if it's not that an invalid MSET hash.

The pattern size SHOULD be a power of two (implementations could likely use faster vectorized loops then).

## Examples

- `0x0242` -> `0x42424242`; repeat a `uint8` equal to `0x42` 4 times
- `0x001234` -> `0x12341234`; repeat a `uint16` equal to `0x1234` 2 times
- `0x7e42` -> `0x42 * 128`; repeat a `uint8` equal to `0x42` 128 times
- `0x7f1234` -> `0x1234 * 129`; repeat a `uint16` equal to `0x1234` 129 times
- `0x800242` -> `0x42 * 256`; repeat a `uint8` equal to `0x42` 258 times
- `0x01123456` -> `0x123456123456123456`; repeat a `uint24` equal to `0x123456123456123456` 3 times
- `0x03` -> `0x0000000000`; zerofill 5 bytes.

## Rational

- Varuint count minus two.
  The varuint count is minus two because counts of 0 and 1 are better served by an identity CIDs, it doesn't make sense to encode them here then.
  Subbing by two allows powers 128 to be stored in one less byte.
- No pattern equal zerofill.
  An empty pattern would lead a multiplication by 0 of the size which would be empty data, however that is better served by identity CIDs.
  We instead reuse this shorter value for something more usefull.
  NUL bytes is the most popular padding value used in most apps, it make sense to grant them this one byte shorter opportunity.
