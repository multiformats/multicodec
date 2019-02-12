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
                # Check for invalid rows
                if len(row) != 4:
                    raise CheckError(f"expected 4 items, got {len(row)}")

                [name, _, code, _] = row

                # Check for a name
                if not name:
                    raise CheckError(f"empty protocol name for code '{code}'")

                # Check code format
                if not code.startswith("0x"):
                    raise CheckError(f"code for '{name}' doesn't start with 0x: '{code}'")

                # Parse the code
                try:
                    code = int(code, 16)
                except Exception as e:
                    raise CheckError(f"failed to parse code '{code}' for '{name}': {e}")

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
