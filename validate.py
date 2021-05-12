#!/usr/bin/env python3

import csv
import sys
import re

# We have some duplicates
ALIAS_TABLE = [
    {"ipfs", "p2p"},
]

def check(fname='table.csv'):
    class CheckError(Exception):
        pass

    aliases = {}
    for nameset in ALIAS_TABLE:
        for name in nameset:
            aliases[name] = nameset

    success = True
    with open(fname) as table:
        tablereader = csv.reader(table, strict=True, skipinitialspace=False)
        codes = {}
        names = {}
        headerOffsets = []
        lastCode = -1
        for line, row in enumerate(tablereader):
            try:
                # Check the padding of each column
                offset = 0
                for col, item in enumerate(row):
                    le = len(item)
                    if col == 0:  # first column 0 has no padding
                        offset = le
                        continue
                    offset = offset + le
                    thisOffset = offset - len(item.lstrip())
                    if line == 0:  # header line sets the standard
                        headerOffsets.append(thisOffset)
                    elif col < len(headerOffsets) or le != 0:
                        if thisOffset != headerOffsets[col - 1]:
                            raise CheckError(f"bad spacing at column {col}")

                # Skip the header
                if line == 0:
                    continue

                # Check for invalid rows
                if len(row) != 5:
                    raise CheckError(f"expected 4 items, got {len(row)}")

                [name, _, code, _, _] = row

                # Check for a name
                if not name:
                    raise CheckError(f"empty protocol name for code '{code}'")

                # Check code format
                if not re.match(r"^\s*0x([0-9a-f][0-9a-f])+$", code):
                    raise CheckError(f"code for '{name}' does not look like a byte sequence: '{code}'")

                # Check name format
                if not re.match(r"^[a-z][a-z0-9_-]+$", name):
                    raise CheckError(f"name '{name}' violates naming restrictions")

                # Parse the code
                try:
                    code = int(code, 16)
                except Exception as e:
                    raise CheckError(f"failed to parse code '{code}' for '{name}': {e}")

                # Check codes are ascending
                ooo = code < lastCode
                lastCode = code
                if ooo:
                    raise CheckError(f"code {code} is out of order, previous code was {lastCode}")

                # Finally, check for duplicates

                if name in names:
                    raise CheckError(f"found duplicate {name}: {code} and {names[name]}")
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

                # Reserved Code Range: Private Use Area – Do not permit any codes in this range
                if code in range(0x300000, 0x400000):
                    raise CheckError(
                        f"found code in Private Use Area: {hex(code)} with name '{name}'"
                    )
            except CheckError as e:
                success = False
                print(f"row {line}: {e}", file=sys.stderr)

    return success

if __name__ == "__main__":
    if not check():
        sys.exit(1)
