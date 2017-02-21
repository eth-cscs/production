# Compiling your code

## Cray Systems

Regardless of which programming environment (compiler suite) you are using, you should always compile code with the Cray wrapper commands (`cc` for C code, `CC` for C++ code and `ftn` for Fortran code). The compiler wrappers produce statically-linked executables by default; for dynamic libraries use the `-dynamic` flag or `export CRAYPE_LINK_TYPE=dynamic` before building.
Note that dynamical linking is the default when the cudatoolkit module is loaded. You should include the compiler flags appropriate to the underlying compiler suite (Intel, GNU, PGI, Cray). There are also specific options for the wrappers themselves: see the man pages of `ftn`, `cc`, and `CC` for details.

For example, to compile a Fortran code on the system: `ftn [options] code.f90 -o code`. For C code: `cc [options] code.c -o code`, and for C++ code: `CC [options] code.cpp -o code`. Note that MPI, BLAS and LAPACK are all found automatically, if needed.

