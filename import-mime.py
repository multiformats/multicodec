#!/usr/bin/env python

import csv
import os
import urllib.request
import xml.etree.ElementTree as ET

sections = {
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

ns = {'a': 'http://www.iana.org/assignments'}
source = "https://www.iana.org/assignments/media-types/media-types.xml"


class Table(list):
    def __init__(self, fname='table.csv'):
        self._fname = fname
        with open(fname) as table:
            self.extend(csv.reader(table, skipinitialspace=True))

    def save(self):
        widths = {}
        for row in self:
            for i, cell in enumerate(row):
                if len(cell) > widths.get(i, 0):
                    widths[i] = len(cell)

        formatted = ((("" if i == 0 else " " *
                       (1 + widths[i - 1] - len(row[i - 1]))) + cell
                      for i, cell in enumerate(row)) for row in self)

        tmpfname = self._fname + ".tmp"
        with open(tmpfname, 'w') as table:
            writer = csv.writer(table)
            writer.writerows(formatted)
        os.rename(tmpfname, self._fname)


def formatCode(code: int) -> str:
    nbytes = 0
    if code == 0:
        nbytes = 1
    else:
        remaining = code
        while remaining > 0:
            remaining >>= 7
            nbytes += 1

    return f"0x{code:0{nbytes*2}x}"


def main():
    table = Table("table.csv")
    lastCode = sections.copy()
    assigned = {}
    mimeStart = 0
    mimeEnd = 0
    for mimeStart, [_, tag, _, _] in enumerate(table[1:]):
        if tag == "mimetype":
            break
    else:
        mimeStart += 1

    mimeStart += 1  # initial offset

    for mimeEnd, [name, tag, code,
                  description] in enumerate(table[mimeStart:]):
        if tag != "mimetype":
            break

        code = int(code, 16)

        assigned[name] = (code, description)

        parts = name.split('/')
        section = parts[0]
        if section not in sections:
            raise RuntimeError(f"unknown mime base type {name}")
        if len(parts) == 1:
            continue
        elif len(parts) != 2:
            raise RuntimeError(f"invalid mimetype {name}")

        subtype = parts[1]
        lastCode[section] += 1
        if code & 0xff0000 != sections[section]:
            raise RuntimeError(f"wrong section for type")
        if lastCode[section] != code:
            raise RuntimeError(
                f"expected code 0x{lastCode[section]:x}, got 0x{code:x}")
    else:
        mimeEnd += 1

    mimeEnd += mimeStart  # initial offset

    for [_, tag, _, _] in table[mimeEnd:]:
        if tag == "mimetype":
            raise RuntimeError(
                f"did not expect an mimetype out of the mime range")

    with urllib.request.urlopen(source) as f:
        root = ET.parse(f).getroot()

    if root.get("id") != "media-types":
        raise RuntimeError("expected root node to have id 'media-types'")

    for mimetype in root.iterfind(
            './a:registry/a:record/a:file',
            ns,
    ):
        mimetype = mimetype.text
        if mimetype in assigned:
            continue
        [section, subtype] = mimetype.split('/', 1)
        code = lastCode[section] + 1
        lastCode[section] = code
        assigned[mimetype] = (code, "")

    items = [(code, name, description)
             for name, (code, description) in assigned.items()]
    items.sort(key=lambda item: item[0])
    table[mimeStart:mimeEnd] = [(name, "mimetype", formatCode(code),
                                 description)
                                for (code, name, description) in items]
    table.save()


if __name__ == "__main__":
    main()
