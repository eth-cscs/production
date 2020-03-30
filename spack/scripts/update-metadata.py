#!/usr/bin/env python3

import copy
import os
import re
import subprocess
import yaml


def get_spack_path(path):
    return os.path.dirname(os.path.realpath(__file__)).split("scripts")[0] + path


def main():
    with open(get_spack_path("dom/packages.yaml"), "r") as infile, open(
        get_spack_path("dom/packages_new.yaml"), "w"
    ) as outfile:
        data = yaml.load(infile, Loader=yaml.FullLoader)
        new_data = copy.deepcopy(data)
        for spack_name, pv in data["packages"].items():
            if spack_name == "mpich":
                # All mpich versions will be mapped to the default cray-mpich module
                cmd = subprocess.run(
                    "module avail cray-mpich", stderr=subprocess.PIPE, shell=True
                )
                regex_default_module = re.compile(r"cray-mpich\/(\S*?)\(default\)\s+")
                default_version = regex_default_module.findall(
                    cmd.stderr.decode("utf-8")
                )
                for mpich_mod in pv["modules"]:
                    new_data["packages"]["mpich"]["modules"][
                        mpich_mod
                    ] = default_version[0]

            elif "modules" in pv:
                # First get the mapping from cray module to spack entry
                module_mappings = {}
                new_modules = {}
                for a, b in pv["modules"].items():
                    try:
                        spack_extras = a.split("%")[1]
                    except IndexError:
                        spack_extras = ""

                    cray_name = b.split("/")[0]
                    if cray_name in module_mappings:
                        module_mappings[cray_name].append(spack_extras)
                    else:
                        module_mappings[cray_name] = [spack_extras]

                for cray_name in set(module_mappings.keys()):
                    cmd = subprocess.run(
                        f"module avail {cray_name}", stderr=subprocess.PIPE, shell=True
                    )
                    regex_available_module = re.compile(
                        cray_name + r"\/(\S*?)(\(default\))?\s+"
                    )
                    available_versions = regex_available_module.findall(
                        cmd.stderr.decode("utf-8")
                    )

                    for (cray_version, _) in available_versions:
                        for spack_specs in module_mappings[cray_name]:
                            if spack_name == "cuda":
                                cuda_version = cray_version.split(".")
                                spack_version = f"{cuda_version[0]}.{cuda_version[1]}"
                            else:
                                spack_version = cray_version

                            full_spack_name = f"{spack_name}@{spack_version}"
                            if spack_specs != "":
                                full_spack_name = f"{full_spack_name}%{spack_specs}"
                            new_modules[full_spack_name] = f"{cray_name}/{cray_version}"

                    default_versions = [
                        v for (v, d) in available_versions if d == "(default)"
                    ]
                    if spack_name == "cuda":
                        cuda_version = default_versions[0].split(".")
                        spack_version = f"{cuda_version[0]}.{cuda_version[1]}"
                    else:
                        spack_version = default_versions[0]

                    new_data["packages"][spack_name]["version"] = [spack_version]

                new_data["packages"][spack_name]["modules"] = new_modules

        yaml.dump(new_data, outfile, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()
