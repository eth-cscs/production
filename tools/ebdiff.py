#!/usr/bin/env python3

#
# A tool to produce diffs between easyconfigs
#
# @author: vkarak

import argparse
import difflib
import glob
import os
import re
import subprocess
import sys
from pathlib import Path


if sys.version_info.minor < 5:
    print(f'{sys.argv[0]}: unsupported Python version: '
          f'found {sys.version_info.major}.{sys.version_info.minor}, '
          f'required >= 3.6')
    sys.exit(2)


def print_specs(matches, *args, **kwargs):
    if not matches:
        print('No relevant easyconfigs were found', *args, **kwargs)
        return

    print('The following relevant easyconfigs were found:', *args, **kwargs)
    for m in matches:
        print(f'    - {m}', *args, **kwargs)


class Spec:
    '''Wrapper for package specs.

    The format is the following
    {pkg_name}@{pkg_version}^{tc_name}@{tc_version}^{suffix}

    Example: GROMACS@2019.2^CrayGNU@19.09^-cuda-10.1

    '''

    def __init__(self, spec):
        package, *rest = spec.split('^', maxsplit=2)
        try:
            pkg_name, pkg_version = package.split('@', maxsplit=1)
        except ValueError:
            pkg_name, pkg_version = package, None

        if len(rest) == 0:
            toolchain, suffix = None, None
        if len(rest) == 1:
            toolchain, suffix = rest[0], None
        elif len(rest) == 2:
            toolchain, suffix = rest[0], rest[1]

        if toolchain:
            try:
                tc_name, tc_version = toolchain.split('@', maxsplit=1)
            except ValueError:
                tc_name, tc_version = toolchain, None
        else:
            tc_name, tc_version = None, None

        self._package_name = pkg_name
        self._package_version = pkg_version
        self._toolchain_name = tc_name
        self._toolchain_version = tc_version
        self._suffix = suffix

    @property
    def package_name(self):
        return self._package_name

    @property
    def package_version(self):
        return self._package_version

    @property
    def toolchain_name(self):
        return self._toolchain_name

    @property
    def toolchain_version(self):
        return self._toolchain_version

    @property
    def suffix(self):
        return self._suffix

    def easyconfig(self):
        ret = self.package_name
        if self.package_version:
            ret += f'-{self.package_version}'

        if self.toolchain_name:
            ret += f'-{self.toolchain_name}'

        if self.toolchain_version:
            ret += f'-{self.toolchain_version}'

        if self.suffix:
            ret += f'{self.suffix}'

        return ret + '.eb'

    def __str__(self):
        ret = self.package_name
        if self.package_version:
            ret += f'@{self.package_version}'

        if self.toolchain_name:
            ret += f'^{self.toolchain_name}'

        if self.toolchain_version:
            ret += f'@{self.toolchain_version}'

        if self.suffix:
            ret += f'^{self.suffix}'

        return ret


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()

    # This is just for the help message
    argparser.add_argument('diff_optons', metavar='DIFF_OPTS',
                           nargs='?', default='-uN')
    argparser.add_argument('package', metavar='PACKAGE')
    argparser.add_argument('spec1', metavar='SPEC1')
    argparser.add_argument('spec2', metavar='SPEC2')
    argparser.add_argument(
        '-r', '--robot-path', metavar='PATH',
        action='append', dest='robot_paths', default=[],
        help="Override EasyBuild's robot path"
    )
    argparser.add_argument(
        '--num-matches', action='store', default=10,
        help='Number of relevant easyconfigs to print in case of unknown specs'
    )
    options, diff_args = argparser.parse_known_args()
    if not diff_args:
        diff_args = ['-uN']

    if not options.robot_paths:
        options.robot_paths = os.getenv('EASYBUILD_ROBOT_PATHS').split(':')

    if not options.robot_paths:
        print('ERROR: no robot path defined', file=sys.stderr)
        sys.exit(2)

    try:
        options.num_matches = int(options.num_matches)
    except ValueError:
        print(f'ERROR: --num-matches not an integer: {num_matches}',
              file=sys.stderr)
        sys.exit(2)

    if options.num_matches < 0:
        print('ERROR: --num-matches must be a positive integer',
              file=sys.stderr)
        sys.exit(2)

    spec1 = Spec(f'{options.package}@{options.spec1}')
    spec2 = Spec(f'{options.package}@{options.spec2}')

    ec1_base = spec1.easyconfig()
    ec2_base = spec2.easyconfig()
    ec1, ec2 = None, None
    for path in options.robot_paths:
        prefix = Path(path)/options.package[0].lower()/options.package
        if ec1 is None:
            ec1 = prefix / ec1_base
            if not ec1.exists():
                ec1 = None
            else:
                print(f'Found matching spec for {spec1}: {ec1}')

        if ec2 is None:
            ec2 = prefix / ec2_base
            if not ec2.exists():
                ec2 = None
            else:
                print(f'Found matching spec for {spec2}: {ec2}')

    if ec1 is None or ec2 is None:
        matches = []
        for path in options.robot_paths:
            prefix = Path(path)/options.package[0].lower()/options.package
            matches += glob.glob(
                f'{prefix}/{options.package}-*.eb'
            )

        do_diff = False
    else:
        do_diff = True

    if ec1 is None:
        print(f'ERROR: unknown spec: {spec1}', file=sys.stderr)

        # Sort matches based on similarity to the requested spec
        print_specs(
            difflib.get_close_matches(
                spec1.easyconfig(),
                (os.path.basename(m) for m in matches),
                n=options.num_matches,
            ), file=sys.stderr
        )

    if ec2 is None:
        print(f'ERROR: unknown spec: {spec2}', file=sys.stderr)

        # Sort matches based on similarity to the requested spec
        print_specs(
            difflib.get_close_matches(
                spec2.easyconfig(),
                (os.path.basename(m) for m in matches),
                n=options.num_matches,
            ), file=sys.stderr
        )

    if not do_diff:
        sys.exit(2)

    diff_cmd = os.getenv('EBDIFF_CMD', '/usr/bin/diff')

    # Split diff_cmd in case users pass arguments to the command
    diff_cmd, *args = diff_cmd.split()
    if args:
        diff_args = args + diff_args

    completed = subprocess.run([diff_cmd, *diff_args, ec1, ec2],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)
    print(completed.stdout, end='')
    if completed.returncode == 2:
        print('ERROR: diff failed', file=sys.stderr)
        print(completed.stderr, file=sys.stderr)

    sys.exit(completed.returncode)
