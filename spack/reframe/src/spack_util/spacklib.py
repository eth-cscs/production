import copy
import re
import semver
import glob
import os
import re


def parse_version(version_str):
    intel_version_style = re.search(r'^(\d+)\.(\d+)\.(\d+)\.(\d+)$', version_str)
    major_minor_style = re.search(r'^(\d+)\.(\d+)$', version_str)
    if intel_version_style:
        major = intel_version_style.group(1)
        minor = intel_version_style.group(2)
        patchlevel = intel_version_style.group(3)
        prerelease = intel_version_style.group(4)
        ret = semver.VersionInfo(major, minor, patchlevel, prerelease)
    elif major_minor_style:
        major = major_minor_style.group(1)
        minor = major_minor_style.group(2)
        ret = semver.VersionInfo(major, minor, 0)
    else:
        ret = semver.VersionInfo.parse(version_str)

    return ret


def get_highest_version(compilers):
    ver = parse_version("0.0.0")
    for version in compilers.keys():
        if ver < parse_version(version):
            ver = parse_version(version)

    return ver


def get_module_available_versions(name, module_path=os.path.join(os.sep, 'opt', 'cray', 'modulefiles')):
    '''Get all available ``name`` modules defined in path ``module_path``.

    :returns: ``list`` on success.
    '''
    available_modules_files = glob.glob(os.path.join(module_path, name, '*'))
    available_modules = [os.path.basename(m) for m in available_modules_files if not ".version" in m]

    return available_modules


def get_cdts_modulerc_files(include_cdts=[r'cdt/']):
    '''Get all available modulerc files defined inside the cdt modules, expect for the ``include_cdts`` cdts.

    :returns: ``list`` on success.
    '''
    pe_path = os.path.join(os.sep, 'opt', 'cray', 'pe')

    modulerc_files = glob.glob(os.path.join(pe_path, '*', '*', 'modulerc'))
    for cdt in include_cdts:
        modulerc_files = [m for m in modulerc_files if cdt in m and not 'default' in m]

    return modulerc_files


def get_cdt_info_from_modulerc_file(modulerc_file):
    cdt_regex = re.search(r'pe/(?P<name>\S+)\/(?P<version>\S+)/modulerc', modulerc_file)
    cdt_name = cdt_regex.group('name')
    cdt_version = cdt_regex.group('version')

    return cdt_name, cdt_version


def get_full_cdt_name(cdt_name, cdt_version):
    return cdt_name + '/' + cdt_version


def get_default_package_versions_from_modulerc(package_name, modulerc_file):
    reg = re.compile(package_name + r'/(?P<version>\S+)')
    with open(modulerc_file) as f:
        lines = f.read()
        matches = reg.findall(lines)
        if matches:
            return matches[0]
    raise ValueError(f'cannot get module version for {package_name}')


def get_spack_generated_compilers(compiler_type, spack_compilers):
    ret = {}
    if not 'compilers' in spack_compilers:
        return ret

    for compiler in spack_compilers['compilers']:
        if not 'compiler' in compiler:
            continue
        com = compiler['compiler']

        if not 'spec' in com:
            continue
        spec = com['spec']

        if compiler_type in spec:
            version = spec.split('@')[1]

            # excluding the duplicate entries that have empty modules
            # this happens with the cray supported compilers
            # OS compilers should be included with empty modules entries
            if version in ret:
                if not ret[version]['modules']:
                    ret[version] = com
            else:
                ret[version] = com

    return ret


def get_spack_os_compilers(compiler_type, spack_compilers):
    compilers = get_spack_generated_compilers(compiler_type, copy.deepcopy(spack_compilers))

    compiler_versions = list(compilers.keys())
    for version in compiler_versions:
        if 'modules' in compilers[version]:
            if compilers[version]['modules']:
                compilers.pop(version)

    return compilers


def get_spack_cdt_compilers(compiler_type, spack_compilers):
    compilers = get_spack_generated_compilers(compiler_type, copy.deepcopy(spack_compilers))

    compiler_versions = list(compilers.keys())
    for version in compiler_versions:
        if 'modules' in compilers[version]:
            if not compilers[version]['modules']:
                compilers.pop(version)

    return compilers


def extract_all_spack_generated_packages(spack_packages):
    ret = {}
    if not 'packages' in spack_packages:
        return ret
    pkgs = spack_packages['packages']

    if 'all' in pkgs:
        ret = copy.deepcopy(pkgs['all'])

    return ret


def convert_packages_to_legacy(pkgs):
    oldpkgs = {}
    for spack_name, pkg in pkgs.items():
        oldpkg = {}
        oldpkg['modules'] = {}
        oldpkg['paths'] = {}
        modules = oldpkg['modules']
        paths = oldpkg['paths']
        if 'buildable' in pkg:
            oldpkg['buildable'] = pkg['buildable']
        if 'variants' in pkg:
            oldpkg['variants'] = pkg['variants']

        if 'externals' in pkg:
            externals = pkg['externals']
            for entry in externals:
                if 'spec' in entry:
                    if 'modules' in entry:
                        modules[entry['spec']] = entry['modules'][0]
                    elif 'prefix' in entry:
                        paths[entry['spec']] = entry['prefix']

        if not modules:
            oldpkg.pop('modules')
        if not paths:
            oldpkg.pop('paths')

        if not 'modules' in oldpkg and not 'paths' in oldpkg:
            if 'buildable' in oldpkg:
                oldpkg.pop('buildable')

        if oldpkg:
            oldpkgs.update({spack_name: oldpkg})

    return oldpkgs


def get_spack_pkg_name(pkg_name, pkg_data):
    spack_pkg_name = pkg_name
    if 'name' in pkg_data:
        spack_pkg_name = pkg_data['name']

    return spack_pkg_name


def get_spack_pkg_variant(pkg_data):
    variant = ''
    if 'variants' in pkg_data:
        variant = pkg_data['variants']

    return variant


def get_pkg_properties(pkg_name, pkg_data, pkgs):
    pkg = {}
    spack_pkg_name = get_spack_pkg_name(pkg_name, pkg_data)
    variant = get_spack_pkg_variant(pkg_data)

    if not spack_pkg_name in pkgs:
        if 'buildable' in pkg_data:
            pkg['buildable'] = pkg_data['buildable']

        if 'version' in pkg_data:
            pkg['version'] = pkg_data['version']
    else:
        pkg = pkgs[spack_pkg_name]

    return spack_pkg_name, variant, pkg


def add_to_external(pkg_name, pkg_data, pkg_version, compiler, external_specs):
    ret = {}
    spack_pkg_name = get_spack_pkg_name(pkg_name, pkg_data)
    variant = get_spack_pkg_variant(pkg_data)
    if variant:
        variant = ' ' + variant

    compiler_name = ' %' + compiler if compiler else ''

    if 'version_map' in pkg_data:
        if pkg_version:
            if pkg_version in pkg_data['version_map']:
                pkg_version = pkg_data['version_map'][pkg_version]
            elif 'default' in pkg_data['version_map']:
                pkg_version = pkg_data['version_map']['default']

    if pkg_version:
        name = spack_pkg_name + '@' + pkg_version + variant + compiler_name
    else:
        name = spack_pkg_name + variant + compiler_name

    if not name in external_specs:
        external_specs.add(name)
        ret['spec'] = name
        if 'modules' in pkg_data and pkg_version:
            ret['modules'] = [pkg_data['modules'] + '/' + pkg_version]
        elif 'modules' in pkg_data:
            ret['modules'] = [pkg_data['modules']]

    return ret


def compile_cdt_compilers_list(cdt_compilers, cdt_name, cdt_version, compiler_name):
    full_cdt_name = get_full_cdt_name(cdt_name, cdt_version)
    if full_cdt_name in cdt_compilers:
        cdt_compilers[full_cdt_name].append(compiler_name)
    else:
        cdt_compilers[full_cdt_name] = [compiler_name]


def get_substring_pos_or_lastpos(string, substring, start=None, end=None):
    if start and end:
        cur = string.find(substring, start, end)
    elif start:
        cur = string.find(substring, start)
    elif end:
        cur = string.find(substring, 0, end)
    else:
        cur = string.find(substring)

    if cur != -1:
        return cur
    else:
        return len(string)-1


# This is a hack to extract the compiler from a Spec
# Spack uses a full parser for this
# I won't copy it (too big) and I won't implement one either
def get_compiler_from_spec(spec):
    ret = ''
    if '%' in spec:
        spec += ' '
        end = len(spec)-1
        startp = get_substring_pos_or_lastpos(spec, '%')
        if startp == end:
            return ''
        else:
            startp += 1
            oldcur = get_substring_pos_or_lastpos(spec, ' ', startp)
            cur = get_substring_pos_or_lastpos(spec, '-', startp, oldcur)
            oldcur = min(cur, oldcur)
            cur = get_substring_pos_or_lastpos(spec, '~', startp, oldcur)
            oldcur = min(cur, oldcur)
            cur = get_substring_pos_or_lastpos(spec, '+', startp, oldcur)
            oldcur = min(cur, oldcur)
            ret = spec[startp:oldcur]
    return ret


def generate_compiler_list_for_testing(cdt_types, allowed_compilers):
    modulerc_files =  get_cdts_modulerc_files(include_cdts=cdt_types)

    # TODO  add intel here
    compilers = []
    for modulerc_file in modulerc_files:
        _, cdt_version = get_cdt_info_from_modulerc_file(modulerc_file)
        for compiler in allowed_compilers:
            try:
                compilers.append(compiler + "@" + get_default_package_versions_from_modulerc(compiler, modulerc_file) + '-' + cdt_version)
            except:
                pass

    return compilers


def generate_spec_with_proper_compilers(spec_list, allowed_compilers):
    ret = set()
    for spec in spec_list:
        spec_compiler = get_compiler_from_spec(spec)
        if spec_compiler:
            compilers = [c for c in allowed_compilers if spec_compiler in c]
            for compiler in compilers:
                newspec = spec.replace('%' + spec_compiler, '%' + compiler)
                ret.add(newspec)
        else:
            for compiler in allowed_compilers:
                ret.add(f'{spec} %{compiler}')

    return ret
