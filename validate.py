#!/usr/bin/env python3

import csv
import sys

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
        tablereader = csv.reader(table, skipinitialspace=True)
        codes = {}
        names = {}
        for line, row in enumerate(tablereader):
            # Skip the header
            if line == 0:
                continue

            try:
                # Skip empty rows
                if not row:
                    continue

                # Check for invalid rows
                if len(row) != 3:
                    raise CheckError(f"expected 3 items, got {len(row)}")

                # Skip section headers
                if not row[1] and not row[2]:
                    continue

                # Check code format
                if not row[2].startswith("0x"):
                    raise CheckError(f"code '{row[2]}' doesn't start with 0x")

                name = row[0]
                if not name:
                    raise CheckError(f"empty protocol name")

                # Parse the code
                try:
                    code = int(row[2], 16)
                except Exception as e:
                    raise CheckError(f"failed to parse number '{row[2]}': {e}")

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
            except CheckError as e:
                success = False
                print(f"row {line}: {e}", file=sys.stderr)

    return success

if __name__ == "__main__":
    if not check():
        sys.exit(1)
