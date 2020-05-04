#!/usr/bin/env python3

#
# A tool to produce diffs between easyconfigs
#
# @author: vkarak

import argparse
import glob
import os
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
        print('no possible matching specs were found', *args, **kwargs)
        return

    print('the following candidate specs were found:', *args, **kwargs)
    for m in matches:
        print(f'    - {m}', *args, **kwargs)


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
    options, diff_args = argparser.parse_known_args()
    if not diff_args:
        diff_args = ['-uN']

    if not options.robot_paths:
        options.robot_paths = os.getenv('EASYBUILD_ROBOT_PATHS').split(':')

    if not options.robot_paths:
        print(f'{sys.argv[0]}: ERROR: no robot path defined', file=sys.stderr)
        sys.exit(2)

    ec1_base = f'{options.package}-{options.spec1}.eb'
    ec2_base = f'{options.package}-{options.spec2}.eb'
    ec1, ec2 = None, None
    for path in options.robot_paths:
        prefix = Path(path)/options.package[0].lower()/options.package
        if ec1 is None:
            ec1 = prefix / ec1_base
            if not ec1.exists():
                ec1 = None
            else:
                print(f'Found matching spec for '
                      f'{options.package}@{options.spec1}: {ec1}')

        if ec2 is None:
            ec2 = prefix / ec2_base
            if not ec2.exists():
                ec2 = None
            else:
                print(f'Found matching spec for '
                      f'{options.package}@{options.spec2}: {ec2}')

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
        print(f'ERROR: unknown spec: {options.package}@{options.spec1}',
              file=sys.stderr)
        print_specs(matches, file=sys.stderr)

    if ec2 is None:
        print(f'ERROR: unknown spec: {options.package}@{options.spec2}',
              file=sys.stderr)
        print_specs(matches, file=sys.stderr)

    if not do_diff:
        sys.exit(2)

    diff_cmd = os.getenv('EBDIFF_CMD', '/usr/bin/diff')
    completed = subprocess.run([diff_cmd, *diff_args, ec1, ec2],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)
    print(completed.stdout)
    if completed.returncode == 2:
        print('ERROR: diff failed', file=sys.stderr)
        print(completed.stderr, file=sys.stderr)

    sys.exit(completed.returncode)
