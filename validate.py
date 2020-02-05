#!/usr/bin/env python3

import csv
import re
import sys

# We have some duplicates
ALIAS_TABLE = [
    {"ipfs", "p2p"},
]

mimetypes = {
    "application": 0x200000,
    "audio": 0x210000,
    "font": 0x220000,
    "image": 0x230000,
    "message": 0x240000,
    "model": 0x250000,
    "multipart": 0x260000,
    "text": 0x270000,
    "video": 0x280000,
}

def check(fname='table.csv'):
    class CheckError(Exception):
        pass

    aliases = {}
    for nameset in ALIAS_TABLE:
        for name in nameset:
            aliases[name] = nameset

    success = True
    with open(fname) as table:
        tablereader = csv.reader(table, skipinitialspace=True)
        codes = {}
        names = {}
        for line, row in enumerate(tablereader):
            # Skip the header
            if line == 0:
                continue

            try:
                # Check for invalid rows
                if len(row) != 4:
                    raise CheckError(f"expected 4 items, got {len(row)}")

                [name, tag, code, _] = row

                # Check for a name
                if not name:
                    raise CheckError(f"empty protocol name for code '{code}'")

                # Check code format
                if not re.match(r"^0x([0-9a-f][0-9a-f])+$", code):
                    raise CheckError(f"code for '{name}' does not look like a byte sequence: '{code}'")

                # Parse the code
                try:
                    code = int(code, 16)
                except Exception as e:
                    raise CheckError(f"failed to parse code '{code}' for '{name}': {e}")

                # Check MIME type ranges
                mimerange = (code >= 0x200000 and code < 0x300000)
                mimetag = (tag == "mimetype")

                if mimerange and not mimetag:
                    raise CheckError(f"code 0x{code:x} is in the MIME range but has tag '{tag}'")
                elif not mimerange and mimetag:
                    raise CheckError(f"code 0x{code:x} is not in the MIME range but has tag 'mimetype' ")
                elif mimerange and mimetag:
                    mparts = name.split('/')
                    if mparts[0] not in mimetypes:
                        raise CheckError(f"not a known mimetype {name}")
                    mimeSection = mimetypes[mparts[0]]
                    if len(mparts) == 1:
                        if mimeSection != code:
                            raise CheckError(f"expected code {mimeSection}, got 0x{code:x}")
                    elif len(mparts) == 2:
                        if code & 0xff0000 != mimeSection:
                            raise CheckError(f"expected mimetype '{name}' to be in range 0x{(code & 0xff0000):}-0x{(code|0x00ffff):x}")
                    else:
                        raise CheckError(f"invalid mimetype name {name}")

                # Finally, check for duplicates

                if name in names:
                    raise CheckError(f"found duplicate {name}: 0x{code:x} and 0x{names[name]:x}")
                else:
                    names[name] = code

                if code in codes:
                    dup = codes[code]
                    if name in aliases:
                        if dup in aliases[name]:
                            # Skip aliased names
                            continue
                    raise CheckError(
                        f"found duplicate for code {hex(code)} "
                        f"for '{codes[code]}' and '{name}'"
                    )
                else:
                    codes[code] = name
            except CheckError as e:
                success = False
                print(f"row {line}: {e}", file=sys.stderr)

    return success

if __name__ == "__main__":
    if not check():
        sys.exit(1)
