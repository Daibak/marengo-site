#!/usr/bin/env python

import argparse
import sys
import string

import yaml


class TemplateIndented(string.Template):
    def substitute(*args, **kws):
        if not args:
            raise TypeError("descriptor 'substitute' of 'Template' object "
                            "needs an argument")
        self, *args = args  # allow the "self" keyword be passed
        if len(args) > 1:
            raise TypeError('Too many positional arguments')
        if not args:
            mapping = kws
        elif kws:
            mapping = string._ChainMap(kws, args[0])
        else:
            mapping = args[0]

        # Helper function for .sub()
        def convert(mo):
            # Check the most common path first.
            named = mo.group('named') or mo.group('braced')
            if named is not None:
                indent = mo.start() - mo.string[:mo.start()].rfind('\n') - 1
                return str(mapping[named]).replace('\n', '\n' + indent * ' ')
            if mo.group('escaped') is not None:
                return self.delimiter
            if mo.group('invalid') is not None:
                self._invalid(mo)
            raise ValueError('Unrecognized named group in pattern',
                             self.pattern)
        return self.pattern.sub(convert, self.template)


def main(args, nestingLevel=0):
    definitions = {}

    for fi in args.i:
        ld = yaml.load(fi)

        if ld is not None:
            definitions.update(ld)

    tpl = TemplateIndented(args.templateFile.read())
    outputRecursion = tpl.substitute(definitions)

    for _ in range(nestingLevel):
        outputRecursion = TemplateIndented(outputRecursion).substitute(definitions)

    args.o.write(outputRecursion)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Given template substitutes definitions as json dict, generating a complete file"
    )
    parser.add_argument("templateFile",
                        help="Path to file containing the template(text with $ID as variables)",
                        type=argparse.FileType('r'))
    parser.add_argument("-i", metavar="defintion-file", help="Path to file with definition as JSON dictionary", nargs='*',
                        type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument("-o", metavar="output-file", help="Path to output file",
                        type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()
    main(args, nestingLevel=2)

    for f in args.i:
        f.close()
    args.o.close()
    args.templateFile.close()
