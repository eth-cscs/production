#!/usr/bin/env python3

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

if __name__ == "__main__":
    specs = [
        r'gromacs',
        r'gromacs%',
        r'gromacs%gcc',
        r'gromacs %gcc',
        r'gromacs %gcc ',
        r'gromacs%gcc@9.3.0',
        r'gromacs%gcc-mpi',
        r'gromacs%gcc~mpi',
        r'gromacs%gcc+mpi',
        r'gromacs%gcc -mpi',
        r'gromacs%gcc ~mpi',
        r'gromacs%gcc +mpi',
        r'gromacs%gcc@9.3.0-mpi',
        r'gromacs%gcc@9.3.0~mpi',
        r'gromacs%gcc@9.3.0+mpi',
    ]
    for spec in specs:
        print("'" + spec + "' -> '" + get_compiler_from_spec(spec) + "'")
