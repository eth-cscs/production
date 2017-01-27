# Setup Python

For example, with Python 2.7

```
module load Python/2.7.12-CrayGNU-2016.11
```

## Setup your virtual environment
To create a virtual environment into which your modules will be installed,
you should use the provided `virtualenv` tool:

```
mkdir venv-2.7
virtualenv --system-site-packages venv-2.7
source venv-2.7/bin/activate
```

```
piccinal@daint01:~ $ ll venv-2.7/
drwxr-xr-x 2 piccinal csstaff 4096 May 18 18:01 bin
drwxr-xr-x 2 piccinal csstaff 4096 May 18 18:01 include
drwxr-xr-x 3 piccinal csstaff 4096 May 18 18:01 lib
lrwxrwxrwx 1 piccinal csstaff    3 May 18 18:01 lib64 -> lib
```

---

```
(venv) piccinal@daint01:~ $ which python
/users/piccinal/venv-2.7/bin/python
```

* The option `--system-site-packages` gives the virtual environment access to all modules already installed in the system (e.g numpy, pycuda, ...)
* If you would like to create a completely isolated virtual environment, you should use the ``--no-site-packages`` option instead.


