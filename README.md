# Proyecto para el Instituto de Niños Ciegos y Sordos del Valle del Cauca

Add some description to INCS project

## version

0.0.1

## Getting started

Before starting it is necessary to install the following toolchain on your system:

1. [Git](https://git-scm.com/)
2. [Python 3.8.0](https://www.python.org/downloads/release/python-380/)
3. [Black python (formater)](https://github.com/psf/black)

### Preparing the environment

From your terminal run the following commands:

1.  Clone the repository

```shell
git clone repo-url
```

1.  Go to the project folder

```shell
cd repo-name
```

1.  Install and configure the seed using

```shell
source install.sh {my_project_name}
```

_Add the needed environment variables for local development on the `envars.sh` file_

After the installation you can start your virtual environment with the following command:

```shell
st_{project_name}

# Example
st_{project_name}
```

## Unit tests and linter

Execute

```shell
# Run the whole build automation
pyb -v

# Run  unittests
pyb -v unittest

```

## Run funcitons locally

You can run functions locally with the following command:

```shell
functions_framework --source=YOUR_FILE_PATH --target=FUNCTION_NAME --port=PORT --debug
```

## Guidelines

### Headers

```python
#
# copyright
#

# Dependencies
from example import Example

# file_name.py
# Author: author name
# Description: short file description

def foo():
    pass

```

### Code styles

```python
# Upper camel case for class naming
class MyPythonClass:
    pass

# Underscore for access hints
def public_method(self) -> None:
    pass

def _protected_method(self) -> None:
    pass

def __private_method(self) -> None:
    pass


# Python type hints
def foo(id: int, name: str, custom_type: MyPythonClass) -> None:
     pass
```
