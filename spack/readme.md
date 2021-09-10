# Updating config files

To automatically bump `compilers.yaml` and `packages.yaml` after a system change,
run the reframe script in [reframe](reframe):

```console
git clone https://github.com/eth-cscs/production.git
reframe -c production/spack/reframe -R -x spack_push_config_check -r
```

This skips the step where it opens a PR with the new config. To submit
the new config changes, run

```console
reframe -c production/spack/reframe -Rr
```

## Caveats / TODO

- [ ] The script fails with a user compilers.yaml in `~/.spack`, since no new
      compilers are detected. We should probably start using environments and
      override the config scope (start out with empty `'compilers:':`).
- [ ] Handle changing variant names/values in Spack.
