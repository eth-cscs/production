#!/usr/bin/env python3
import argparse
import string
import sys
import re

tc_pattern = re.compile("toolchain\s*=\s*\{\s*'name'\s*:\s*'(\S*)'\s*,\s*'version'\s*:\s*'(\S*)'\s*}")

dep_regex = lambda mod: f"(\s*)\(\s*'({mod})'\s*,\s*EXTERNAL_MODULE\s*\),"
dep_pattern = re.compile(dep_regex('\S*')) # any module


def parse_tc(file, debug):
    ''' determine toolchain information in supplied EasyBuild config '''
    matches = re.search(tc_pattern, file)

    if matches:
        if debug:
            print("found matches from the config: ", matches.group())
            print("found original toolchain in config: ", matches.group(1))
            print("found original toolchain version in config: ", matches.group(2))
    else:
        raise RuntimeError(f"Couldn't determine toolchain information in supplied EasyBuild config.")

    return matches.group(1), matches.group(2)


def greater_ver(v1, v2):
    ''' compare 2 version strings '''
    v1 = [(int(v) if v.isnumeric() else v) for v in v1.split('.')]
    v2 = [(int(v) if v.isnumeric() else v) for v in v2.split('.')]
    return v1 > v2

def parse_metadata(metadata):
    ''' load a version map of every module in the given metadata '''
    modules = {}
    for line in metadata.readlines():
        if line[0] == '[':
            module = line[1:line.find(']')]
            module = module.split('/')
            module, version = module if len(module) > 1 else (module[0], None)
            # keep a map of major versions to latest available version
            if version is not None:
                majver = version.split('.')[0]
                if module not in modules.keys():
                    version = {majver: version}
                else: # update majver if needed
                    versions = modules[module]
                    if majver not in versions.keys() or greater_ver(version, versions[majver]):
                        versions[majver] = version
                    version = {k:versions[k] for k in sorted(versions.keys())}
            modules[module] = version
    return modules



def main():
    parser = argparse.ArgumentParser(description='Switch toolchain to.')

    parser.add_argument('--debug',
                        type=bool, default=False,
                        help="Print verbose info.")

    parser.add_argument('--toolchain-prefix',
                        required=False,
                        help="Toolchain prefix for validation.")

    parser.add_argument('--version',
                        required=True,
                        help="New toolchain version to use.")

    parser.add_argument('--metadata',
                        type=argparse.FileType('r'), required=False,
                        help="Target metadata.")

    # parser.add_argument('--former-cdt',
    #                     type=argparse.FileType('r'), required=False,
    #                     help="Old CDT modulesrc.")

    parser.add_argument('--filenames',
                        nargs='+', required=True,
                        help="Files to process.")

    args = vars(parser.parse_args())

    if args['debug']:
        print(args)
        print(f"New toolchain is set {args['toolchain_prefix']}*-{args['version']}")

    if args['metadata']:
        modules = parse_metadata(args['metadata'])
        if args['debug']:
            print('Metadata:\n', modules)

    for filename in args['filenames']:
        print(f"Processing EasyBuild config {filename} ...")
        if args['debug']:
            print("The new config will be placed in original directory.")

        with open(filename, "r") as originalconfig:
            ec = originalconfig.read()  # contains newlines.
        if args['debug']:
            print("---- The original config was:\n", ec)

        toolchain, version = parse_tc(ec, args['debug'])

        if args['toolchain_prefix'] and not toolchain.startswith(args['toolchain_prefix']):
            sys.exit(f"Invalid toolchain prefix in {filename}")

        newecfilename = filename.replace(f"{toolchain}-{version}",
                                         f"{toolchain}-{args['version']}")
        if args['debug']:
            print("New config file name will be: ", newecfilename)

        newec = re.sub(tc_pattern,
                       f"toolchain = {{'name': '{toolchain}', 'version': '{args['version']}'}}",
                       ec)

        if args['metadata']:
            # find all external dependencies
            deps = re.findall(dep_pattern, newec)
            if deps is not None:
                if args['debug']:
                    print("External Modules:\n", deps)

                for ws, dep in deps:
                    mod = dep.split('/')[0]
                    if mod in modules.keys():
                        ver = modules[mod]
                        if ver is not None:
                            depver = dep.split('/')[1]
                            majver = depver.split('.')[0]
                            # get latest matching version
                            ver = ver[majver] if majver in ver.keys() else ver.values()[-1]
                            mod = f"{mod}/{ver}"
                        if args['debug']:
                            print(f"Replacing '{dep}' by '{mod}'")
                            print(dep_regex(dep))
                        newec = re.sub(dep_regex(dep), f"{ws}('{mod}', EXTERNAL_MODULE),", newec)

        if args['debug']:
            print("---- New config will be:\n", newec)

        ## Check new toolchain
        _, version = parse_tc(newec, args['debug'])
        if version != args['version']:
            sys.exit("Failed to replace toolchain version.")

        with open(newecfilename, "w") as newconfig:
            newconfig.write(newec)  # contains newlines.

        print("Finished writing new config:", newecfilename)


if __name__ == "__main__":
    main()
