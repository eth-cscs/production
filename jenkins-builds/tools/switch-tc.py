#!/usr/bin/env python
__author__ = 'petar.forai'

import argparse
import string
import re

# matching groups (0) and (1) for toolchain name as in source file and
# toolchain\s=\s\{'name':\s'(\w*)',\s*'version'\s*:\s*'(\d*.\d*.\d*)'\s*}


def main():
    parser = argparse.ArgumentParser(description='Switch toolchain to.')
    parser.add_argument('--filename',
                        required=True,
                        metavar='FILE',
                        help="wich file to operate on.")
    parser.add_argument('--toolchain',
                        required=True,
                        metavar='TC',
                        help="toolchain to switch to.")
    parser.add_argument('--version',
                        required=True,
                        metavar='VERSION',
                        help="toolchain version to use.")

    args = vars(parser.parse_args())

    print args
    print "Will use EasyBuild config %s." % (args['filename'])
    print "New toolchain is set %s %s" % (args['toolchain'], args['version'])
    print "The new config will be placed in this directory."

    with open(args['filename'], "r") as originalconfig:
        ec = originalconfig.read()  # contains newlines.
    print "----"
    print "The original config was:\n %s" % (ec)

    # <GPP> updated regex to accept '.' on the version
    tcpattern = re.compile("toolchain\s=\s\{'name':\s'(\S*)',\s*'version'\s*:\s*'(\S*)'\s*}")

    matches = re.search(tcpattern, ec)

    if matches:
        print "found matches from the config: ", matches.group()
        print "found original toolchain in config: ", matches.group(1)
        print "found original toolchain version in config: ", matches.group(2)
    else:
        print "Couldn't determine toolchain information in supplied EasyBuild config."

    oldecfilename = args['filename']
    if not ((args['toolchain'] == 'dummy') and (args['version'] == 'dummy')):
        newecfilename = oldecfilename.replace(matches.group(1), args['toolchain'])
        newecfilename = newecfilename.replace(matches.group(2), args['version'])
    else:
        newecfilename = oldecfilename.replace('-' + matches.group(1), '')
        newecfilename = newecfilename.replace('-' + matches.group(2), '')
        print "Dummy toolchain specified. Taking care of proper naming."

    print "New config file name will be: ", newecfilename

    oldec = string.replace(ec, matches.group(1), args['toolchain'])
    newec = string.replace(oldec, matches.group(2), args['version'])

    print "New config will be: ", newec

    with open(newecfilename, "w") as newconfig:
        newconfig.write(newec)  # contains newlines.

    print "Finished writing new config."


if __name__ == "__main__":
    main()
